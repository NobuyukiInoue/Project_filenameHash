import glob
import hashlib
from msvcrt import getch
import os
import sys
import time

def main():
    argv = sys.argv
    argc = len(argv)

    if argc < 3:
        print("Usage: python %s [hash | unhash] [target_path/target_filename] [output list filename]" %(argv[0]))
        exit(0)

    '''argv check
    for i in range(len(argv)):
        print("argv[" + str(i) + "] = %s" %argv[i])
    '''

    mode = argv[1]
    target_full_path = argv[2].replace("\\", "/")
    pos_filenameStart = target_full_path.rfind("/")
    work_path = target_full_path[0:pos_filenameStart]
    file_pattern = target_full_path[pos_filenameStart + 1:]

    if not os.path.exists(work_path):
        print("%s not found..." %work_path)
        exit(0)

    if argc >= 4:
        filenames_Listfile = argv[3]
    else:
        pos_last_dir = work_path.rfind("/")
        if pos_last_dir >= 0:
            filenames_Listfile = "flist_" + work_path[pos_last_dir + 1:] + ".txt"
        else:
            filenames_Listfile = "flist.txt"

    print("mode = %s" %mode)
    print("target path = %s" %work_path)
    print("filename pattern = %s" %file_pattern)

    if mode == "hash":
        if os.path.exists(filenames_Listfile):
            firstKey = ''
            while (firstKey != 'Y' and firstKey != 'N'):
                print("\n%s is exists. overwrite? (Y/N)" %filenames_Listfile, end = "")
                keyRet = ord(getch())
                firstKey = chr(keyRet).upper()

            print()
            if (firstKey == 'N'):
                print("quit....")
                exit(0)

        flist_hash(work_path, file_pattern, filenames_Listfile)

    elif mode == "unhash":
        if not os.path.exists(filenames_Listfile):
            print("%s is not found." %filenames_Listfile)
            exit(0)
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
    count = 0
    for line in filenames_list:
        flds = line.strip().replace("\"", "").split(",")
        if len(flds) != 2:
            print("split() error ... %s" %line)
            exit(0)
        os.rename(flds[0], flds[1])
        count += 1
    print("\n%d files was renamed to hashed filename." %count)

def rename_to_unhashed_filename(filenames_list):
    count = 0
    for line in filenames_list:
        flds = line.strip().replace("\"", "").split(",")
        if len(flds) != 2:
            print("split() error ... %s" %line)
            exit(0)
        os.rename(flds[1], flds[0])
        count += 1
    print("\n%d files was renamed to original filename." %count)

if __name__ == "__main__":
    main()
