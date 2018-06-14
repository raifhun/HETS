import h5py
import numpy as np
import array
import tkinter as tk
from tkinter import filedialog
# initialize tkinter
root = tk.Tk()
root.withdraw()


def gather_groups(current_file):  # create list of groups in a file
    groups = []
    for key in current_file.keys():
        groups.append(key)
    return groups


def gather_sets(current_file, group):  # create list of sets in a group
    sets = []
    for key in current_file[group].keys():
        sets.append(key)
    return sets


def gather_attributes(current_file, group, current_set):  # get attribute of a set
    attribute_set = []
    for key in current_file[group+"/"+current_set].attrs:
        attribute_set.append(key)
    return attribute_set


def spectrum_extract(current_file):  # extract the histograms and sum them per attribute into one array of values
    group_set = gather_groups(current_file)
    local_data_formatted = []
    line_to_write = []
    for group in group_set:
        sets = gather_sets(current_file, group)
        x = 0
        for current_set in sets:
            attribute_set = gather_attributes(current_file, group, current_set)
            if x == 0:
                line_to_write.append(str(current_file).rsplit('/', 1)[-1])
                print(attribute_set)
                print(group)
                for i in range(0, 2):
                    line_to_write.append(" , ")
                local_data_formatted.append(line_to_write)
                line_to_write = attribute_set
                line_to_write.append("Amplitude")
                local_data_formatted.append(line_to_write)
            x += 1
            line_to_write = []
            for attribute in attribute_set:
                line_to_write.append(current_file[group+"/"+current_set].attrs.get(attribute))
            if x == 1:
                line_to_write = line_to_write[:-1]
            line_to_write.append(current_file[group+"/"+current_set][0:1998:1].sum())
            local_data_formatted.append([line_to_write])
            line_to_write = []
            # print(local_data_formatted)
    return local_data_formatted


def decay_extract(current_file):  # extracts the hdf5 data in a format to read out the decay characteristics
    group_set = gather_groups(current_file)
    local_data_formatted = []
    line_to_write = []
    hist_totals = []
    wl_range = []
    last_set = ""
    for group in group_set:
        sets = gather_sets(current_file, group)
        x = 0
        for current_set in sets:
            print(current_set)
            if x == 0:
                hist_totals = []
                for j in range(0, len(current_file[group+"/"+current_set])):
                    hist_totals.append([j, 0])
                print(hist_totals)

                wl_range.append(current_file[group + "/" + current_set].attrs.get("Em"))
                line_to_write.append(str(current_file).rsplit('/', 1)[-1])
                for i in range(0, 2):
                    line_to_write.append(" , ")
                local_data_formatted.append(line_to_write)
            x += 1
            line_to_write = []
            for i in range(0, len(current_file[group + "/" + current_set])):
                hist_totals[i][1] += current_file[group + "/" + current_set][i]
            last_set = current_set
        wl_range.append(current_file[group + "/" + last_set].attrs.get("Em"))
        local_data_formatted.append(["Wavelength Start", "Wavelength End"])
        local_data_formatted.append([wl_range[0], wl_range[1]])
        print(wl_range)
        for line in hist_totals:
            local_data_formatted.append(line)

        return local_data_formatted


def write_to_file(total_data_entry, dat_file_final, file_list):  # writes the array that was built to an excel file
    number_file = len(total_data_entry)
    max_len = 0
    print(number_file)
    for item in total_data_entry:
        if max_len < len(item):
            max_len = len(item)
    for i in range(0, max_len):
        for j in range(0, number_file):
            print(i)
            if i < len(total_data_entry[j]):
                for k in range(0, len(total_data_entry[j][i])):
                    line_to_write = str(total_data_entry[j][i][k]).replace("]", "").replace("[", "")
                    dat_file_final.write(line_to_write)
                    dat_file_final.write(" , ")
            if i >= len(total_data_entry[j]):
                for k in range(0, len(total_data_entry[j][0])):
                    dat_file_final.write(" , ")
            dat_file_final.write(" , ")
        dat_file_final.write("\n")
    dat_file_final.close()


def main_extraction_loop():  # logic that runs the extraction, can be replaced with gui/improved program control logic
    # logic to collect files that will be extracted
    x = False
    file_list = []
    while x == False:
        root.attributes("-topmost", True)  # just ensures the popup takes focus
        file_list.append(h5py.File(filedialog.askopenfilename(title="Select a File for Extraction",
                                                              filetypes=(("hdf5 files", "*.hdf5"),
                                                                         ("all files", "*.*")))))
        root.attributes("-topmost", False)
        continue_select = input("Would you like to continue adding files (y or n)?")
        if continue_select == "y" or continue_select == "Y" or continue_select == "Yes":
            x = False
        else:
            x = True

    # specify save location for .dat file with results from extraction
    root.attributes("-topmost", True)
    dat_file_path = filedialog.asksaveasfile(title="Select a Save Location",
                                             filetypes=(("dat files", "*.dat"), ("all files", "*.*")),
                                             defaultextension='.dat')
    dat_file_final = open(dat_file_path.name, 'w+')

    # specify which type of extraction this is
    process_type = input("What process would you like? 1 - Spectrum, 2 - Decay, 3 - Specific Decay")
    total_data_entry = []

    # determine the process type you want, sum of wavelength, decay characteristics,
    # or decay characteristics of a certain line, it will now
    if int(process_type) != 1 and int(process_type) != 2 and int(process_type) != 3:
        print("That is not a process number, please start over.")

    if int(process_type) == 1:  # if process 1, runs spectrum extraction
        for file in file_list:
            total_data_entry.append(spectrum_extract(file))
        write_to_file(total_data_entry, dat_file_final, file_list)
        print("Files successfully Extracted")

    if int(process_type) == 2:  # if process 2, runs the decay extraction
        for file in file_list:
            total_data_entry.append(decay_extract(file))
        write_to_file(total_data_entry, dat_file_final, file_list)
        print("Files successfully Extracted")
    if int(process_type) == 3:  # if process 3, runs the decay extraction for specific wavelengths per group
        for file in file_list:
            total_data_entry.append(specific_extract(file))
        write_to_file(total_data_entry, dat_file_final)
        print("Files successfully Extracted")


main_extraction_loop()

