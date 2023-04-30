# Plot hive-style triangle plot of minimap2-derived 
# pairwise alignement with xmatchview.
#
# minimap2: https://github.com/lh3/minimap2
# xmatchview: https://github.com/bcgsc/xmatchview

import os, subprocess

project_path = "/home/USER/PROJECT/"
prefix = project_path + "pairwise_aln/"
apps = "/home/USER/apps/xmatchview"
app_hive = apps + "/xmatchview-hive.py"

files = {
    "accession1": 125047,
    "accession2": 125071,
    "accession3": 125004,
    "accession4": 126202,
    "accession5": 126884,
    "accession6": 127884,
    "accession7": 127732
}

variants = [
    ("accession1", "accession2", "accession3"),
    ("accession4", "accession2", "accession3"),
    ("accession6", "accession7", "accession1"),
    ("accession1", "accession2", "accession5"),
    ("accession3", "accession4", "accession5"),
    ("accession1", "accession2", "accession7")
]

for variant in variants:
    first = variant[0]
    second = variant[1]
    third = variant[2]
    variant_name = first + "__" + second + "__" + third + "__mm2"
    schemae = [
        (first, second),
        (second, first),
        (first, third),
        (third, first),
        (third, second),
        (second, third)
    ]

    print("\nProcessing variant", variant)
    os.makedirs(prefix + variant_name + "/dot", exist_ok=True)
    os.chdir(prefix + variant_name)

    config_list = []
    for i, val in enumerate([first, second, third]):
        # enumerate has 0-based indices, convert them to 1-based ones
        sample = val + ":" + str(files[val])
        i = i + 1
        config_list.append(str(i) + ":" + sample)
        with open(val + ".txt", "w") as s:
            s.write(sample)
    config_body = '\n'.join(config_list)
    with open('config.txt', "w") as config:
        config.write(config_body)
    
    for schema in schemae:
        target = schema[0]
        query = schema[1]
        print("Starting to align...", "\ttarget:", target, "\tquery:", query)
        aln = subprocess.run(["minimap2",
                              "-x", "asm20",
                              prefix + target + ".fna",
                              prefix + query + ".fna",
                              "-N200",
                              "-p0.0001",
                              "-o", target + "_2_" + query + ".paf"],
                        stdout=subprocess.PIPE, stderr = subprocess.PIPE)
        # check the output of the PGA script
        if aln.returncode != 0:
            if aln.stdout:
                standard_output = aln.stdout.decode('utf-8')
                print(standard_output)
            if aln.stderr:
                standard_error = aln.stderr.decode('utf-8')
                print(standard_error)
        
        os.chdir(prefix + variant_name)
    
    print("Current working directory:", os.getcwd())
    print("Starting plot for variant", variant)
    plot = subprocess.run(["python", app_hive,
                           "-q", first  + ".txt",
                           "-r", second + ".txt",
                           "-s", third + ".txt",
                           "-x", second + "_2_" + first + ".paf",
                           "-y", third + "_2_" + first + ".paf",
                           "-z", second + "_2_" + third + ".paf",
                           "-i", "0",
                           "-b", "1",
                           "-c", "78",
                           "-a", "0.75"], 
                        stdout=subprocess.PIPE, stderr = subprocess.PIPE)
    print("python", app_hive, "-q", first  + ".txt", "-r", second + ".txt", "-s", third + ".txt", "-x", first + "_2_" + second + ".paf", "-y", first + "_2_" + third + ".paf", "-z", third + "_2_" + second + ".paf", "-i", "0", "-b", "1", "-c", "80", "-a", "0.75")
    if plot.returncode == 0:
            if plot.stdout:
                standard_output = plot.stdout.decode('utf-8')
                print(standard_output)
            if plot.stderr:
                standard_error = plot.stderr.decode('utf-8')
                print(standard_error)
    os.listdir(os.curdir)
    os.chdir(prefix)
