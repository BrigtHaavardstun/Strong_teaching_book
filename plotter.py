def extract_info(filename):
    data = []
    with open(filename, 'r') as f:
        all_lines = f.read().split("\n")
        for line in all_lines:
            parts = line.split(",")
            if parts == [""]:
                continue
            data.append((parts[-2],parts[-1]))

    

    with open(filename[:-4]+ "_data_extract.csv", 'w') as f:
        data = [line[0] + "," + line[1] for line in data]
        f.write("\n".join(data))
    


def plots_of_py(filename):
    x_values = []
    y_values = []
    with open(filename, 'r') as f:
        all_lines= f.read().split("\n")
        for line in all_lines:
            concept, witness = list(map(int, line.split(",")))
            x_values.append(witness)
            y_values.append(concept)

    import matplotlib.pyplot as plt
    plt.scatter(x_values, y_values,color="blue")
    plt.plot(list(range(8)),list(range(8)),color="red")
    plt.xlabel("Witness size")
    plt.ylabel("Concept size")
    plt.show()


if __name__ == '__main__':
    extract_info("TeachingBookPB.csv")
    plots_of_py("TeachingBookPB_data_extract.csv")