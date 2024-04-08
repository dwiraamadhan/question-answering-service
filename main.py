from functions.question_answering import process_answer

def main():
    # Bagian utama program
    print("Halo, ini adalah program Python sederhana.")
    nama = input("Siapa namamu? ")
    print("Halo,", nama, "! Selamat datang.")

    question = ("what is bni direct?")
    result = process_answer(question)
    print(result)



# Memanggil fungsi main
if __name__ == "__main__":
    main()