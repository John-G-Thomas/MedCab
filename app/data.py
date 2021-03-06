""" StrainData for MedCab Project
Data Science Unit 4 Build Week
Robert Sharp
August 2020
"""
from collections import defaultdict
from typing import List
from Fortuna import random_value, FlexCat
from pandas import read_csv


class StrainData:
    """ Primary Data Object for MedCab """

    __slots__ = (
        'data', 'effect_lookup', 'flavor_lookup', 'type_lookup', 'id_lookup',
        'name_lookup', 'random_by_type', 'random_by_effect', 'random_by_flavor',
    )

    def __init__(self, filename):
        # Temporary Raw Data
        df = read_csv(filename)
        df['Type'] = df['Type'].str.title()
        df['Flavors'] = df['Flavors'].str.replace('/', ',')
        df['Strain'] = df['Strain'].apply(self._fix_string)
        df['Description'] = df['Description'].apply(self._fix_string)

        # Initialize Lookup Tables
        self.data = df.to_dict(orient='records')      # List[Dict {Key: Value}]
        self.effect_lookup = defaultdict(list)        # Dict {Key: List[String]}
        self.flavor_lookup = defaultdict(list)        # Dict {Key: List[String]}
        self.type_lookup = defaultdict(list)          # Dict {Key: List[String]}
        self.name_lookup = dict()                # Dict {Key: Dict {Key: Value}}
        self.id_lookup = defaultdict(list)

        # Populate Lookup Tables
        for strain in self.data:
            strain['Nearest'] = self._names_by_ids(strain['Nearest'].split(','))
            strain['Nearest'].remove(strain['Strain'])
            strain['Effects'] = strain['Effects'].split(',')
            for effect in strain['Effects']:
                self.effect_lookup[effect].append(strain['Strain'])

            strain['Flavors'] = strain['Flavors'].split(',')
            for flavor in strain['Flavors']:
                self.flavor_lookup[flavor].append(strain['Strain'])

            self.type_lookup[strain['Type']].append(strain['Strain'])
            self.name_lookup[strain['Strain']] = strain

        # Setup Randomizers
        self.random_by_type = FlexCat(
            {k: v for k, v in self.type_lookup.items()},
            val_bias='truffle_shuffle',
        )
        self.random_by_effect = FlexCat(
            {k: v for k, v in self.effect_lookup.items()},
            val_bias='truffle_shuffle',
        )
        self.random_by_flavor = FlexCat(
            {k: v for k, v in self.flavor_lookup.items()},
            val_bias='truffle_shuffle',
        )

    def random_strain(self) -> dict:
        """ Returns a random Strain
        @return: dict
        """
        return random_value(self.data)

    def effects_list(self) -> List[str]:
        """ List of all Effects
        @return: List[str]
        """
        return list(self.effect_lookup.keys())

    def types_list(self) -> List[str]:
        """ List of all Types
        @return: List[str]
        """
        return list(self.type_lookup.keys())

    def flavors_list(self) -> List[str]:
        """ List of all Flavors
        @return: List[str]
        """
        return list(self.flavor_lookup.keys())

    def strain_by_id(self, idx: str) -> dict:
        """ Strain lookup by Index
        @param idx: str
        @return: dict
        """
        return self.data[int(idx)]

    def strain_by_name(self, name: str) -> dict:
        """ Strain lookup by Name
        @param name: str
        @return: dict
        """
        return self.name_lookup[name]

    def strains_by_type(self, strain_type: str) -> List[str]:
        """ List of Strains of the desired Type
        @param strain_type: str
        @return: List[str]
        """
        return self.type_lookup[strain_type]

    def strains_by_effect(self, effect: str) -> List[str]:
        """ List of Strains that produce the desired Effect
        @param effect: str
        @return: List[str]
        """
        return self.effect_lookup[effect]

    def strains_by_flavor(self, flavor: str) -> List[str]:
        """ List of Strains that have the desired Flavor
        @param flavor: str
        @return: List[str]
        """
        return self.flavor_lookup[flavor]

    def _names_by_ids(self, ids):
        """ Returns a list of names based on a list of ids, internal only
        @param ids: list of ids
        @return: list of names
        """
        return [self.data[int(idx)]['Strain'] for idx in ids]

    @staticmethod
    def _fix_string(string: str) -> str:
        """ Unicode Field Medic Solution, internal only
        @param string: str
        @return: str
        """
        return string.replace(
            '\u2018', "'",
        ).replace(
            '\u2019', "'",
        ).replace(
            '\u201c', "'",
        ).replace(
            '\u201d', "'",
        ).replace(
            '\u00f1', "n",
        ).replace(
            '\u2013', "-",
        ).replace(
            '\u2014', "-",
        ).replace(
            '\u014d', "o",
        ).replace(
            '\u2026', '-',
        ).replace(
            '\u0101', 'a',
        )
