import os

def rename_files():
  # (1) get file names from given folder
  file_list = os.listdir(r'/Users/eriknguyen/workspace/35_nano/01_/prank')
  saved_path = os.getcwd()
  print("cwd = " + saved_path)
  os.chdir(r'/Users/eriknguyen/workspace/35_nano/01_/prank')
  print(os.getcwd())

  # (2) for each file, rename filename
  translation_table = dict.fromkeys(map(ord, '0123456789'), None)
  for file_name in file_list:
    os.rename(file_name, file_name.translate(translation_table))
    print(file_name)

rename_files()