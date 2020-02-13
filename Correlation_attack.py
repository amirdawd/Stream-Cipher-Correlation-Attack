import matplotlib.pyplot as plt


def lfsr_1(initiate_state, key_stream_length, polynomial):
    result = []
    key = initiate_state
    for i in range(0, key_stream_length):
        feedback = (((key[0]) + (key[2]) + (key[3]) + (key[6]) + (key[7]) + (key[9]) + (key[11]) + (key[12])) % 2)
        key = key[1:]
        key.append(feedback)
        result.append(key[-1])
    return result


def lfsr_2(initiate_state, key_stream_length, polynomial):
    result = []
    key = initiate_state
    for i in range(0, key_stream_length):
        feedback = (((key[0]) + (key[2]) + (key[4]) + (key[5]) + (key[8]) + (key[9]) + (key[11]) + (key[13])) % 2)
        key = key[1:]
        key.append(feedback)
        result.append(key[-1])
    return result


def lfsr_3(initiate_state, key_stream_length, polynomial):
    result = []
    key = initiate_state
    for i in range(0, key_stream_length):
        feedback = (((key[0]) + (key[1]) + (key[4]) + (key[7]) + (key[9]) + (key[12]) + (key[13]) + (key[15])) % 2)
        key = key[1:]
        key.append(feedback)
        result.append(key[-1])
    return result


def key_stream_generator(key_stream, key_size, polynomial):
    form = ''
    p_max = 0
    deviation = 0
    deviation_list = []
    k_temp = None
    integer = 0
    if key_size == 13:
        form = '013b'
        for state in range(0, 2 ** key_size):
            key_i = [int(x) for x in format(state, form)]
            generate_seq = lfsr_1(key_i, len(key_stream), polynomial)
            p_temp = correlation(key_stream, generate_seq, len(key_stream))
            temp_deviation = abs(p_temp - 0.5)
            if temp_deviation > deviation:
                k_temp = key_i
                deviation = temp_deviation
                p_max = p_temp
                integer = state
            deviation_list.append(temp_deviation)
    elif key_size == 15:
        form = '015b'
        for state in range(0, 2 ** key_size):
            key_i = [int(x) for x in format(state, form)]
            generate_seq = lfsr_2(key_i, len(key_stream), polynomial)
            p_temp = correlation(key_stream, generate_seq, len(key_stream))
            temp_deviation = abs(p_temp - 0.5)
            if temp_deviation > deviation:
                k_temp = key_i
                deviation = temp_deviation
                p_max = p_temp
                integer = state
            deviation_list.append(temp_deviation)
    elif key_size == 17:
        form = '017b'
        for state in range(0, 2 ** key_size):
            key_i = [int(x) for x in format(state, form)]
            generate_seq = lfsr_3(key_i, len(key_stream), polynomial)
            p_temp = correlation(key_stream, generate_seq, len(key_stream))
            temp_deviation = abs(p_temp - 0.5)
            if temp_deviation > deviation:
                k_temp = key_i
                deviation = temp_deviation
                p_max = p_temp
                integer = state
            deviation_list.append(temp_deviation)

    return k_temp, p_max, deviation_list,integer


def hamming_distance(u, z):
    distance = 0
    if len(u) != len(z):
        print("The length must be the same")
        return ''
    else:
        for x in range(0, len(u)):
            if int(u[x]) != int(z[x]):
                distance += 1
    return distance


def correlation(u, z, N):
    return 1 - ((hamming_distance(u, z)) / N)


def verify_sequence(initial_1, initial_2, initial_3, final_stream, N):
    out_put = []
    for x in range(0, N):
        if initial_1[x] + initial_2[x] + initial_3[x] > 1:
            out_put.append(1)
        else:
            out_put.append(0)
    return hamming_distance(out_put, final_stream), correlation(out_put, final_stream, N), out_put


def plot(x_value, y_value, x_label, y_label, image_name):
    plt.plot(x_value, y_value, 'ro')
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.legend(loc='best')
    plt.savefig(image_name)
    plt.show()


def main():
    key_file = open('key_stream.txt', 'r')
    key_stream = ''
    for x in key_file:
        key_stream += str(x)
    output = []
    for x in key_stream:
        output.append(x)
    print(output)
    c_1 = [1, 0, 1, 1, 0, 0, 1, 1, 0, 1, 0, 1, 1]
    c_2 = [1, 0, 1, 0, 1, 1, 0, 0, 1, 1, 0, 1, 0, 1, 0]
    c_3 = [1, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 1, 0, 1, 0]
    k_1, p_max_1, deviation_list_1,state = key_stream_generator(output, 13, c_1)
    print("PROCESSING THE SIMULATION!!!...")
    k_2, p_max_2, deviation_list_2,state2 = key_stream_generator(output, 15, c_2)
    k_3, p_max_3, deviation_list_3,state3 = key_stream_generator(output, 17, c_3)
    # plot k1
    print("Plotting graph...")
    plot([x for x in range(0, 2 ** 13)], deviation_list_1, 'Iteration of different states',
         'Highest deviation from 1/2', 'K1')
    print("The initial state for K_1 is: ", k_1, p_max_1, state)
    # plot k2
    print("Plotting graph...")
    plot([x for x in range(0, 2 ** 15)], deviation_list_2, 'Iteration of different states',
         'Highest deviation from 1/2', 'K2')
    print("The initial state for K_2 is: ", k_2, p_max_2,state2)
    # plot k3
    print("Plotting graph...")
    plot([x for x in range(0, 2 ** 17)], deviation_list_3, 'Iteration of different states',
         'Highest deviation from 1/2', 'K3')
    print("The initial state for K_3 is: ", k_3, p_max_3,state3)
    print("Verifying the output....")
    N = len(output)
    lfsr1 = lfsr_1(k_1, N, c_1)
    lfsr2 = lfsr_2(k_2, N, c_2)
    lfsr3 = lfsr_3(k_3, N, c_3)
    print("The Hamming distance is :", verify_sequence(lfsr1, lfsr2, lfsr3, output, N))
    print("Done")


if __name__ == "__main__":
    state= [0,1]
    for x in range(0,36):
        temp = state[0]
        state[0] = state[1]
        feedback = (temp + state[0]) % 2
        state[-1] = feedback
        print(feedback)
