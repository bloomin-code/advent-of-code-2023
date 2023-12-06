use std::fs::read_to_string;

use nom::IResult;
use rayon::prelude::*;

#[derive(Debug, Clone, Default)]
struct Mapper {
    length: u64,
    source: u64,
    destination: u64,
}

impl Mapper {
    #[inline]
    pub fn map_to_destination(&self, i: u64) -> u64 {
        if self.in_range(i) {
            let dist = i - self.source;
            self.destination + dist
        } else {
            i
        }
    }

    pub fn in_range(&self, i: u64) -> bool {
        self.source <= i && i < self.source + self.length
    }
}

#[derive(Debug, Clone, Default)]
struct Lookup(Vec<Mapper>);

impl Lookup {
    #[inline]
    pub fn map_to_destination(&self, i: u64) -> u64 {
        for mapper in &self.0 {
            if mapper.in_range(i) {
                return mapper.map_to_destination(i);
            }
        }
        i
    }
}


#[derive(Debug, Clone, Default)]
struct Table {
    seed_to_soil: Lookup,
    soil_to_fertilizer: Lookup,
    fertilizer_to_water: Lookup,
    water_to_light: Lookup,
    light_to_temperature: Lookup,
    temperature_to_humidity: Lookup,
    humidity_to_location: Lookup,
}

impl Table {
    #[inline]
    pub fn map_to_destination(&self, i: u64) -> u64 {
        let soil = self.seed_to_soil.map_to_destination(i);
        let fertilizer = self.soil_to_fertilizer.map_to_destination(soil);
        let water = self.fertilizer_to_water.map_to_destination(fertilizer);
        let light = self.water_to_light.map_to_destination(water);
        let temperature = self.light_to_temperature.map_to_destination(light);
        let humidity = self.temperature_to_humidity.map_to_destination(temperature);
        self.humidity_to_location.map_to_destination(humidity)
    }
}

#[derive(Debug, Clone, Default)]
struct InputData {
    seeds: Vec<u64>,
    table: Table
}

fn parse(input: &str) -> IResult<&str, InputData> {
    use nom::{
        bytes::complete::tag,
        character::complete::{line_ending, space1, u64, anychar},
        combinator::map,
        multi::{many_till, separated_list1},
        sequence::{preceded, pair, separated_pair, tuple}
    };
    let seeds = preceded(tag("seeds: "), separated_list1(space1, u64));
    let mapper = map(tuple((u64, space1, u64, space1, u64)), |(destination, _, source, _, length)| {
        Mapper { destination, source, length }
    });
    let mappers = separated_list1(line_ending, mapper);
    let lookup_id = many_till(anychar, line_ending);
    let lookup = map(pair(lookup_id, mappers), |((id, _), mappers)| {
        (id.into_iter().collect::<String>(), Lookup(mappers))
    });
    let table = separated_list1(pair(line_ending, line_ending), lookup);
    let mut parser = map(separated_pair(seeds, pair(line_ending, line_ending), table), |(seeds, table)| {
        let mut my_table = Table::default();
        for (id, lookup) in table {
            match id.as_ref() {
                "seed-to-soil map:" => my_table.seed_to_soil = lookup,
                "soil-to-fertilizer map:" => my_table.soil_to_fertilizer = lookup,
                "fertilizer-to-water map:" => my_table.fertilizer_to_water = lookup,
                "water-to-light map:" => my_table.water_to_light = lookup,
                "light-to-temperature map:" => my_table.light_to_temperature = lookup,
                "temperature-to-humidity map:" => my_table.temperature_to_humidity = lookup,
                "humidity-to-location map:" => my_table.humidity_to_location = lookup,
                _ => unreachable!("Invalid lookup table")
            }
        }
        InputData { seeds, table: my_table }
    });

    parser(input)
}

fn main() {
    let input = read_to_string("input.txt").expect("Should have input file");
    let (_, InputData { seeds, table }) = parse(&input).unwrap();
    let closest = seeds.iter().map(|seed| table.map_to_destination(*seed)).min().expect("Some data");
    println!("Part 1: {closest}");
    let closest = seeds.par_chunks(2).map(|v| (v[0]..(v[0] + v[1]))).flatten().map(|seed| table.map_to_destination(seed)).min().expect("Some data");
    println!("Part 2: {closest}");
}

#[cfg(test)]
mod test {
    use super::*;

    #[test]
    fn test_part1() {
        let input = "seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4";
        let (_, output) = parse(input).unwrap();
        let output_str = format!("{output:#?}");
        let example = InputData {
    seeds: vec![
        79,
        14,
        55,
        13,
    ],
    table: Table {
        seed_to_soil: Lookup(
            vec![
                Mapper {
                    length: 2,
                    source: 98,
                    destination: 50,
                },
                Mapper {
                    length: 48,
                    source: 50,
                    destination: 52,
                },
            ],
        ),
        soil_to_fertilizer: Lookup(
            vec![
                Mapper {
                    length: 37,
                    source: 15,
                    destination: 0,
                },
                Mapper {
                    length: 2,
                    source: 52,
                    destination: 37,
                },
                Mapper {
                    length: 15,
                    source: 0,
                    destination: 39,
                },
            ],
        ),
        fertilizer_to_water: Lookup(
            vec![
                Mapper {
                    length: 8,
                    source: 53,
                    destination: 49,
                },
                Mapper {
                    length: 42,
                    source: 11,
                    destination: 0,
                },
                Mapper {
                    length: 7,
                    source: 0,
                    destination: 42,
                },
                Mapper {
                    length: 4,
                    source: 7,
                    destination: 57,
                },
            ],
        ),
        water_to_light: Lookup(
            vec![
                Mapper {
                    length: 7,
                    source: 18,
                    destination: 88,
                },
                Mapper {
                    length: 70,
                    source: 25,
                    destination: 18,
                },
            ],
        ),
        light_to_temperature: Lookup(
            vec![
                Mapper {
                    length: 23,
                    source: 77,
                    destination: 45,
                },
                Mapper {
                    length: 19,
                    source: 45,
                    destination: 81,
                },
                Mapper {
                    length: 13,
                    source: 64,
                    destination: 68,
                },
            ],
        ),
        temperature_to_humidity: Lookup(
            vec![
                Mapper {
                    length: 1,
                    source: 69,
                    destination: 0,
                },
                Mapper {
                    length: 69,
                    source: 0,
                    destination: 1,
                },
            ],
        ),
        humidity_to_location: Lookup(
            vec![
                Mapper {
                    length: 37,
                    source: 56,
                    destination: 60,
                },
                Mapper {
                    length: 4,
                    source: 93,
                    destination: 56,
                },
            ],
        ),
    },
};
        let example_str = format!("{example:#?}");
        assert_eq!(output_str, example_str);
        let InputData { seeds, table } = output;
        let closest = seeds.iter().map(|seed| table.map_to_destination(*seed)).min().expect("Some data");
        assert_eq!(closest, 35);
}
}
