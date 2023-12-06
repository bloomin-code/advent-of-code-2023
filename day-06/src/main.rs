use std::fs::read_to_string;

use nom::IResult;
use rayon::prelude::*;

#[derive(Debug, Clone, Default)]
struct RaceStat {
    time: u64,
    record: u64,
}

impl RaceStat {
    fn margins(&self) -> usize {
        (0..=self.time).into_iter().filter(|held_time| {
            let run_time = self.time - held_time;
            let distance = held_time * run_time;
            distance > self.record
        }).count()
    }
}

#[derive(Debug, Clone, Default)]
struct InputData {
    races: Vec<RaceStat>
}

fn parse(input: &str) -> IResult<&str, InputData> {
    use nom::{
        bytes::complete::tag,
        character::complete::{line_ending, space1, u64},
        combinator::map,
        multi::separated_list1,
        sequence::{preceded, pair, separated_pair}
    };
    let times = preceded(pair(tag("Time:"), space1), separated_list1(space1, u64));
    let distances = preceded(pair(tag("Distance:"), space1), separated_list1(space1, u64));
    let mut parser = map(separated_pair(times, line_ending, distances), |(times, distances)| {
        InputData {
            races: times.into_iter()
                .zip(distances.into_iter())
                .map(|(time, record)| RaceStat { time, record })
                .collect()
        }
    });
    parser(input)
}

fn part1(InputData { races }: &InputData) -> usize {
    races.iter().map(|race| race.margins()).product()
}

fn part2(InputData { races }: &InputData) -> usize {
    let mut time: String = "".to_string();
    let mut record: String = "".to_string();
    for r in races {
        time += &r.time.to_string();
        record += &r.record.to_string();
    }
    let race = RaceStat {
        time: time.parse().unwrap(),
        record: record.parse().unwrap(),
    };
    race.margins()
}

fn main() {
    let input = read_to_string("input.txt").expect("Should have input file");
    let (_, output) = parse(&input).unwrap();
    let p1 = part1(&output);
    println!("Part 1: {p1}");
    let p2 = part2(&output);
    println!("Part 2: {p2}");
}

#[cfg(test)]
mod test {
    use super::*;

    #[test]
    fn test_part1() {
        let input = "Time:      7  15   30
Distance:  9  40  200";
        let (_, output) = parse(input).unwrap();
        let output_str = format!("{output:#?}");
        let example = InputData {
            races: vec![
                RaceStat {
                    time: 7,
                    record: 9
                },
                RaceStat {
                    time: 15,
                    record: 40,
                },
                RaceStat {
                    time: 30,
                    record: 200,
                }
            ]
        };
        let example_str = format!("{example:#?}");
        assert_eq!(output_str, example_str);
        assert_eq!(part1(&output), 288);
        assert_eq!(part2(&output), 71503);
    }
}
