use std::error::Error;
use std::fs::File;
use std::io::prelude::*;
use std::iter::zip;

fn read_in_local_file(path: &str) -> Result<String, Box<dyn Error>> {
    let mut file = File::open(path)?;
    let mut contents = String::new();
    file.read_to_string(&mut contents)?;
    Ok(contents)
}

fn return_string_as_number(str_vector: Vec<char>) -> u32 {
    if str_vector.len() == 0 {
        return 0;
    }
    let str_number: String = str_vector.iter().collect();
    println!("{}", str_number);
    let existing_numbers: Vec<&str> = [
        "one", "two", "three", "four", "five", "six", "seven", "eight", "nine",
    ]
    .to_vec();
    for (index, number) in existing_numbers.iter().enumerate() {
        if str_number.contains(number) {
            return (index + 1) as u32;
        }
    }
    return 0;
}
fn main() {
    let contents = read_in_local_file("src/input_1.txt").unwrap();
    let contents_list: Vec<&str> = contents.split("\n").collect();
    let mut first_numbers: Vec<char> = Vec::new();

    for content in contents_list {
        let mut five_char_buffer = Vec::new();
        for char in content.chars() {
            five_char_buffer.push(char);
            let char_from_string = return_string_as_number(five_char_buffer.clone());
            if char_from_string != 0 {
                first_numbers.push((b'0' + char_from_string as u8) as char);
                println!("{}", (b'0' + char_from_string as u8) as char);
                break;
            }
            // if char is digit
            if char.is_digit(10) {
                first_numbers.push(char);
                break;
            }
            if five_char_buffer.len() > 5 {
                five_char_buffer.remove(0);
            }
        }
    }
    let contents_list: Vec<&str> = contents.split("\n").collect();
    let mut second_numbers: Vec<char> = Vec::new();
    for content in contents_list {
        let mut five_char_buffer = Vec::new();
        for char in content.chars().rev() {
            five_char_buffer.push(char);
            let mut reversed_buffer = five_char_buffer.clone();
            reversed_buffer.reverse();
            let char_from_string = return_string_as_number(reversed_buffer);
            if char_from_string != 0 {
                second_numbers.push((b'0' + char_from_string as u8) as char);
                break;
            }
            // if char is digit
            if char.is_digit(10) {
                second_numbers.push(char);
                break;
            }
            if five_char_buffer.len() > 5 {
                five_char_buffer.remove(0);
            }
        }
    }

    let mut sum: u32 = 0;
    for (first, second) in zip(first_numbers, second_numbers) {
        let combined = format!("{}{}", first, second);
        println!("{}", combined);
        sum += combined.parse::<u32>().unwrap();
    }
    println!("Sum: {}", sum);
}
