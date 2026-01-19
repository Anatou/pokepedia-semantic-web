export interface Pokemon {
    num: number;
    pk: string;
    type1: string;
    type2?: string;
    gen: string;
    famille: string;
    url: string;
    image?: string;
}

export interface Node {
  id: number,
  label: string
}

export interface Edge {
  id: number,
  from: number,
  to: number
}

export type GroupType = 'type1' | 'type2' | 'all-types' | 'generation' | 'famille' | 'none';

export type Coverage = {
  advantages: string[],
  disadvantages: string[]
};

export interface PokemonWithCoverage {
  pokemons: Pokemon[];
  coverage: Coverage;
}