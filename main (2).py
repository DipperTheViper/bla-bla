import pandas as pd



if __name__ == '__main__':
    columns = dict()
    dissimilarity_matrix = None
    features = pd.DataFrame(columns=['name', 'type', 'domain'])
    numeric_features_details = pd.DataFrame(
        columns=['name', 'mean', 'median', 'mode', 'variance', 'std'])

    f = open('./KDDTest-21.arff.txt', 'r').readlines()
    csv_file = open('file.csv', 'w')

    for line in f:
        if line[0] == '@':
            if line[:10] == "@attribute":
                if line[-2] == '}':
                    # tozih
                    attr_type = 'Binary' if line[-11:-
                                                 1] == "{'0', '1'}" else 'Nominal'
                elif line[-5:-1] == "real":
                    # tozih
                    attr_type = 'Numeric'
                else:
                    print('error')
                    exit()
                # tozih
                attr_name = line[12:12 + line[12:].find('\'')]
                columns[attr_name] = attr_type

            elif line[:5] == "@data":
                csv_file.write(','.join(list(columns.keys())) + '\n')
            else:
                continue
        else:
            csv_file.write(line)

    df = pd.read_csv('file.csv')

    for key in columns:
        # tozih
        domain = f'{df[key].min()}-{df[key].max()}' if columns[key] == 'Numeric' else 'None'
        features = features.append(
            {'name': key, 'type': columns[key], 'domain': domain}, ignore_index=True, sort=False)

    for key in features[features['type'] == 'Numeric']['name']:
        numeric_features_details = numeric_features_details.append(
            {'name': key, 'mean': df[key].mean(), 'median': df[key].median(),
             'mode': df[key].mode()[0], 'variance': df[key].var(),
             'std': df[key].std()}, ignore_index=True, sort=False)


    output_file = open('./output.txt', 'w')
    output_file.write(features.to_csv(index=False) +
                      '\n' +
                      numeric_features_details.to_csv(index=False))
    print("Well Done!")
    csv_file.close()
    output_file.close()
