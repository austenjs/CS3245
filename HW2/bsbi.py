from typing import List
import os

class BSBI:
    '''
    A class that contains helper functions to implement BSBI.

    Attributes:
    num_of_files_in_one_block (int): Number of files in a block
    filenames (List[str]): Number of filenames
    '''

    def __init__(self, num_of_files_in_one_block, filenames):
        self.num_of_files_in_one_block = num_of_files_in_one_block
        self.filenames = filenames

    def generate_chunks(self) -> List[List[int]]:
        '''
        Generate chunks of filenames.

        Return:
        A list of lists, where the i-th list denotes the i-th chunk.
        '''
        chunks = []
        for i in range(0, len(self.filenames), self.num_of_files_in_one_block):
            chunks.append(self.filenames[i: i + self.num_of_files_in_one_block])
        return chunks

    def merge(self, list_of_filenames, target_folder, target_level):
        '''
        Do 2-way merge on the filenames.

        Argument:
        list_of_filenames (list[str]): A list of filenames
        target_folder (str): Path to save the merged file
        target_level (int): Denote the level of the merging, act as identifier
        '''
        number_of_merging = len(list_of_filenames) // 2
        for i in range(number_of_merging):
            # Open 2 files that is going to be merged
            filename0, filename1 = list_of_filenames[2 * i : 2 * i + 2]
            file0 = open(os.path.join(target_folder, filename0), 'r')
            file1 = open(os.path.join(target_folder, filename1), 'r')

            # Open target file
            target_name = os.path.join(target_folder, 'level{}_chunk{}.txt'.format(target_level, i))
            target_file = open(os.path.join(target_folder, target_name), 'w')

            # Perform merging
            line0 = file0.readline().rstrip()
            line1 = file1.readline().rstrip()
            while line0 != '' and line0 != '\n' and line1 != '' and line1 != '\n':
                termId0 = int(line0.split("|", 1)[0])
                termId1 = int(line1.split("|", 1)[0])
                if termId0 < termId1:
                    target_file.write(line0)
                    target_file.write("\n")
                    line0 = file0.readline().rstrip()
                elif termId0 > termId1:
                    target_file.write(line1)
                    target_file.write("\n")
                    line1 = file1.readline().rstrip()
                else:
                    target_file.write(str(termId0))
                    elem_line0 = list(map(int, line0.split('|')[1:]))
                    elem_line1 = list(map(int, line1.split('|')[1:]))
                    m, n = len(elem_line0), len(elem_line1)
                    i = j = 0
                    while i < m and j < n:
                        if elem_line0[i] < elem_line1[j]:
                            target_file.write("|" + str(elem_line0[i]))
                            i += 1
                        else:
                            target_file.write("|" + str(elem_line1[j]))
                            j += 1

                    # Leftovers
                    while i < m:
                        target_file.write("|" + str(elem_line0[i]))
                        i += 1
                    while j < n:
                        target_file.write("|" + str(elem_line1[j]))
                        j += 1
                    target_file.write("\n")
                    line0 = file0.readline().rstrip()
                    line1 = file1.readline().rstrip()
                
            # Left overs of file0
            while line0 != '' and line0 != '\n':
                target_file.write(line0)
                target_file.write("\n")
                line0 = file0.readline().rstrip()

            # Left overs of file1
            while line1 != '' and line1 != '\n':
                target_file.write(line1)
                target_file.write("\n")
                line1 = file1.readline().rstrip()

            # Delete the old 2 files
            file0.close()
            file1.close()
            os.remove(os.path.join(target_folder, filename0))
            os.remove(os.path.join(target_folder, filename1))
