def generate_subtitles(input_file, output_file, max_duration=3, max_characters=30):
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    def split_text(text):
        if len(text) <= max_characters:
            return [text]
        else:
            # Split by words and join words until length exceeds max_characters
            words = text.split()
            chunks = []
            current_chunk = ""
            for word in words:
                if len(current_chunk) + len(word) + 1 <= max_characters:
                    current_chunk += word + " "
                else:
                    chunks.append(current_chunk.strip())
                    current_chunk = word + " "
            chunks.append(current_chunk.strip())
            return chunks

    with open(output_file, 'w', encoding='utf-8') as f:
        start_time = 0
        subtitle_index = 1
        for line in lines:
            line = line.strip()
            chunks = split_text(line)
            for chunk in chunks:
                start_minutes, start_seconds = divmod(int(start_time), 60)
                start_milliseconds = int((start_time % 1) * 1000)

                end_time = min(start_time + max_duration, start_time + len(chunk) / 10)  # Assuming 10 characters per second
                end_minutes, end_seconds = divmod(int(end_time), 60)
                end_milliseconds = int((end_time % 1) * 1000)

                subtitle = f"{subtitle_index}\n{start_minutes:02d}:{start_seconds:02d},{start_milliseconds:03d} --> {end_minutes:02d}:{end_seconds:02d},{end_milliseconds:03d}\n{chunk}\n\n"
                f.write(subtitle)

                start_time = end_time
                subtitle_index += 1

if __name__ == "__main__":
    input_filename = "result.txt"  # Replace with the name of your input text file
    output_filename = "output.srt"  # Replace with the desired output subtitle file name
    generate_subtitles(input_filename, output_filename)
