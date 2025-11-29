from timeit import timeit


def compute_lps(pattern):
    lps = [0] * len(pattern)
    length = 0
    i = 1

    while i < len(pattern):
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        else:
            if length != 0:
                length = lps[length - 1]
            else:
                lps[i] = 0
                i += 1

    return lps


def kmp_search(text, pattern):
    pattern_length = len(pattern)
    text_length = len(text)

    lps = compute_lps(pattern)

    i = 0
    j = 0

    while i < text_length:
        if pattern[j] == text[i]:
            i += 1
            j += 1
        elif j != 0:
            j = lps[j - 1]
        else:
            i += 1

        if j == pattern_length:
            return i - j

    return -1


def build_shift_table(pattern):
    table = {}
    length = len(pattern)

    for index, char in enumerate(pattern[:-1]):
        table[char] = length - index - 1

    table.setdefault(pattern[-1], length)
    return table


def boyer_moore_search(text, pattern):
    shift_table = build_shift_table(pattern)
    i = 0

    while i <= len(text) - len(pattern):
        j = len(pattern) - 1

        while j >= 0 and text[i + j] == pattern[j]:
            j -= 1

        if j < 0:
            return i

        i += shift_table.get(text[i + len(pattern) - 1], len(pattern))

    return -1


def polynomial_hash(s, base=256, modulus=101):
    n = len(s)
    hash_value = 0
    for i, char in enumerate(s):
        power_of_base = pow(base, n - i - 1) % modulus
        hash_value = (hash_value + ord(char) * power_of_base) % modulus
    return hash_value


def rabin_karp_search(text, pattern):
    pattern_length = len(pattern)
    main_string_length = len(text)

    base = 256
    modulus = 101

    pattern_hash = polynomial_hash(pattern, base, modulus)
    current_slice_hash = polynomial_hash(text[:pattern_length], base, modulus)

    h_multiplier = pow(base, pattern_length - 1) % modulus

    for i in range(main_string_length - pattern_length + 1):
        if pattern_hash == current_slice_hash:
            if text[i:i+pattern_length] == pattern:
                return i

        if i < main_string_length - pattern_length:
            current_slice_hash = (current_slice_hash - ord(text[i]) * h_multiplier) % modulus
            current_slice_hash = (current_slice_hash * base + ord(text[i + pattern_length])) % modulus
            if current_slice_hash < 0:
                current_slice_hash += modulus

    return -1


def load_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def main():
    texts = {
        'Text 1': load_file('text1.txt'),
        'Text 2': load_file('text2.txt')
    }

    searching_algorithms = {
        'KMP Search': kmp_search,
        'Boyer-Moore Search': boyer_moore_search,
        'Rabin-Karp Search': rabin_karp_search
    }

    patterns = {
        'Short existing': 'пошук',
        'Short non-existing': 'Lorem',
        'Long existing': 'replace me',
        'Long non-existing': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit'
    }

    for title, text in texts.items():
        print(f"\nProcessing {title}...")
        for name, search_func in searching_algorithms.items():
            print(f"\nUsing {name}:")
            for pattern_name, pattern in patterns.items():
                if pattern_name == 'Long existing':
                    pattern = text[-2000:-1945] # match a long non-existing substring length

                time_taken = timeit(lambda: search_func(text, pattern), number=1)
                print(f" - {pattern_name}: {time_taken:.6f} seconds")


if __name__ == "__main__":
    main()
