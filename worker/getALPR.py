from openalpr import Alpr


def get_license(file_name):
    l = []
    alpr = Alpr('us', '/etc/openalpr/openalpr.conf', '/usr/share/openalpr/runtime_data')
    results = alpr.recognize_file(file_name)
    if len(results['results']) == 0:
        print("Can't find a plate in image:", file_name)
    else:
        for i in range(len(results['results'][0]['candidates'])):
            l.append([results['results'][0]['candidates'][i]['plate'],results['results'][0]['candidates'][i]['confidence']])
    return l
