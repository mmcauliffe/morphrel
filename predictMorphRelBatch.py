import os

import multiprocessing
import subprocess

thisdir = r'C:\Users\michael\Documents\GitHub\morphrel'

big_file = os.path.join(thisdir,'pairwise_s_S_scores_sem.txt')
reout_file = os.path.join(thisdir,'pairwise_s_S_scores_sem_rem.txt')
script = os.path.join(thisdir,'predictMorphRel.r')

num_procs = 6

num_lines = 170000

def do_work(filenum):
    path = os.path.join(thisdir,'%d.txt' % filenum)
    com = ['Rscript',script,path]
    proc = subprocess.Popen(com,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    out,errs = proc.communicate()
    if errs:
        print(str(errs.decode()))
    num = int(str(out.decode()).split(' ')[1])
    return num

def test_do_work():
    print(do_work(2))

def remove_dups():
    pairs = set([])
    num_duplicates = 0
    cur_file = 0
    lines_for_out = list()
    words_with_alt = 0
    total_words = 0
    with open(big_file,'r') as f:
        with open(reout_file,'w') as outf:
            for line in f:
                total_words += 1
                l = line.split('\t')
                if (l[0],l[1]) in pairs:
                    num_duplicates += 1
                else:
                    pairs.update([(l[0],l[1])])
                    outf.write(line)

    print(num_duplicates,total_words,num_duplicates/total_words)

def process_morph_rel():
    pool = multiprocessing.Pool(processes=num_procs)
    cur_file = 0
    lines_for_out = list()
    words_with_alt = 0
    total_pairs = 0
    words = set()
    with open(reout_file,'r') as f:
        for line in f:
            l = line.split('\t')
            if l[0] == l[1]:
                continue
            words.add(l[0])
            words.add(l[1])
            total_pairs += 1
            lines_for_out.append(line)
            if len(lines_for_out) > num_lines:
                with open(os.path.join(thisdir,'%d.txt' % cur_file),'w') as outf:
                    outf.writelines(lines_for_out)
                lines_for_out = list()
                cur_file += 1
                if cur_file == num_procs:
                    res = pool.map(do_work,range(num_procs))
                    for r in res:
                        words_with_alt += r

                    cur_file = 0
            if total_pairs % (num_lines * 10) == 0:
                print(words_with_alt,total_pairs)
    if len(lines_for_out) > 0:
        with open(os.path.join(thisdir,'%d.txt' % cur_file),'w') as outf:
            outf.writelines(lines_for_out)
        cur_file += 1
        res = pool.map(do_work,range(cur_file))
        for r in res:
            words_with_alt += r
    print(words_with_alt,total_pairs,words_with_alt/total_pairs)
    print('total number of words: ', len(words))

def do_blah():
    import re
    from collections import Counter
    words = Counter()
    blah_dir = os.path.join(thisdir,'blah')
    files = os.listdir(blah_dir)
    for f in files:
        with open(os.path.join(blah_dir,f),'r') as f:
            for line in f:
                if not line:
                    continue
                l = re.split('\s+',line)
                words.update(l[:2])
    print(len(words))
    print(sum(1 for k,v in words.items() if v > 1))

if __name__ == '__main__':
    #remove_dups()
    #process_morph_rel()
    #test_do_work()
    do_blah()
