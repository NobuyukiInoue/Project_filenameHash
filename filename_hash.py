import glob
import hashlib
import os
import sys
import time

def main():
    argv = sys.argv
    argc = len(argv)

    if (argc < 3):
        print("Usage: python %s [hash | unhash] <work_path/filename> [filename_list]" %(argv[0]))
        exit(0)

    elif (argc < 4):
        filenames_Listfile = "flist.txt"
    else:
        filenames_Listfile = argv[3]

    '''argv check
    for i in range(len(argv)):
        print("argv[" + str(i) + "] = %s" %argv[i])
    '''

    mode = argv[1]
    pos_filenameStart = argv[2].replace("\\", "/").rfind("/")
    work_path = argv[2][0:pos_filenameStart]
    file_pattern = argv[2][pos_filenameStart + 1:]

    if not os.path.exists(work_path):
        print("%s not found..." %work_path)
        exit(0)

    print("mode = %s" %mode)
    print("target path = %s" %work_path)
    print("filename pattern = %s" %file_pattern)

    if mode == "hash":
        flist_hash(work_path, file_pattern, filenames_Listfile)
    elif mode == "unhash":
        flist_unhash(filenames_Listfile)

def flist_unhash(filename_listfile):
    filename_list = load_flist(filename_listfile)

    # all file rename
    rename_to_unhashed_filename(filename_list)

def flist_hash(work_path, file_pattern, filenames_listfile):
    '''
    current_filename rename to hashed_filename
    '''
    # get filename filename list
    # flist = glob.glob(work_path + "/" + file_pattern, recursive=True)
    flist = glob.glob(work_path + "/" + file_pattern)
    
    filenames_list = []
    for fname in flist:
        hashed_filename = hashlib.md5(fname.encode('sjis')).hexdigest()
        filenames_list.append("\"" + fname + "\",\"" + work_path + "/" + hashed_filename + "\"\n")

    # print(filenames_list)
    save_flist(filenames_listfile, filenames_list)

    # all file rename
    rename_to_hashed_filename(filenames_list)

def load_flist(loadfilename):    
    with open(loadfilename, mode='r') as f:
        filename_list = f.readlines()
    return filename_list

def save_flist(savefilename, filenames_list):
    with open(savefilename, mode='w') as f:
        f.writelines(filenames_list)

def rename_to_hashed_filename(filenames_list):
    for line in filenames_list:
        flds = line.strip().replace("\"", "").split(",")
        if len(flds) != 2:
            print("split() error ... %s" %line)
            exit(0)
        os.rename(flds[0], flds[1])

def rename_to_unhashed_filename(filenames_list):
    for line in filenames_list:
        flds = line.strip().replace("\"", "").split(",")
        if len(flds) != 2:
            print("split() error ... %s" %line)
            exit(0)
        os.rename(flds[1], flds[0])

if __name__ == "__main__":
    main()
