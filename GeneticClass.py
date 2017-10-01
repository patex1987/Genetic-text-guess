'''
Created on 1. 10. 2017

@author: patex1987
'''

import string
import random


class Member(object):
    '''
    Member class containing:
    - member name
    - member success score
    '''
    def __init__(self, member_name, success_score=0.0):
        '''
        Member initialization
        '''
        self.member_name = member_name
        self.success_score = success_score

    def __str__(self):
        '''
        string representation of the Member object
        '''
        return 'Name:{0}\tScore:{1}'.format(self.member_name,
                                            self.success_score)


class Population(object):
    '''
    genetic Population with evolution features
    TODO: the parameters has to be described
    '''
    def __init__(self,
                 secret_word,
                 population_limit=200,
                 default_population_count=10,
                 best_percent=0.2,
                 rest_percent=0.2,
                 min_children=2,
                 max_children=10,
                 mutate_element_count=2,
                 mutation_probability_coeff=5):
        '''
        Initializing the object parameters
        '''
        self._secret_word = secret_word
        self._secret_word_length = len(self._secret_word)
        self._population_limit = population_limit
        self._char_set = self._generate_char_set()
        self._default_population_count = default_population_count
        self.actual_population = self._generate_default_population()
        self.result_found = False
        self._best_percent = best_percent
        self._rest_percent = rest_percent
        self._best_count = int(self._default_population_count *
                               self._best_percent)
        self._rest_count = int(self._default_population_count *
                               self._rest_percent)
        self._best_selected = list()
        self._rest_selected = list()
        self._rest_fill = list()
        self._min_children = min_children
        self._max_children = max_children
        self._mutate_element_count = mutate_element_count
        self._mutation_probability_coeff = mutation_probability_coeff

    def _generate_char_set(self):
        '''
        Generates the default char set, the members can use for guessing
        to do - the char_set should be improved
        '''
        return list(string.ascii_lowercase) + [' ', '.', '!', ',', ';']

    def _generate_default_population(self):
        '''
        generates default population based on the length of secret word and
        initial population count. Initial success rate is zero
        '''
        return [Member(member_name=''.join([random.choice(self._char_set)
                for _ in range(self._secret_word_length)]))
                for _ in range(self._default_population_count)]

    def member_selection(self):
        '''
        Selection of the members
        '''
        self._eval_success_rate()
        self.actual_population = sorted(self.actual_population,
                                        key=lambda member: member.success_score,
                                        reverse=True)
        self._best_count = int(len(self.actual_population) *
                               self._best_percent)
        self._rest_count = int(len(self.actual_population) *
                               self._rest_percent)
        if self.actual_population[0].member_name == self._secret_word:
            self.result_found = True
        self._best_selected = self.actual_population[:self._best_count]
        rest_set = self.actual_population[self._best_count:]
        self._rest_selected = [random.choice(rest_set)
                               for _ in range(self._rest_count)]
        self._rest_fill = list(set(rest_set) - set(self._rest_selected))

    def summary(self):
        '''
        basic evaluation
        '''
        best_score = sorted(self.actual_population,
                            key=lambda member: member.success_score,
                            reverse=True)[0].success_score
        base_string = 'Population count: {0};' + \
                      'Best score: {1:.2f};' + \
                      'Example guess: {2}'
        return base_string.format(len(self.actual_population),
                                  best_score,
                                  self.actual_population[0].member_name)

    def _eval_success_rate(self):
        '''
        Assigns success score to the actual population
        '''
        for member in self.actual_population:
            member.success_score = self._eval_single_success(member.member_name)

    def _eval_single_success(self, guess):
        '''
        Calculates the success score for a single guess
        '''
        score = 0
        for pos in range(self._secret_word_length):
            if self._secret_word[pos] == guess[pos]:
                score += 1
        return score / self._secret_word_length

    def combination(self):
        '''
        Combines together best set and rest set
        '''
        population_selector = self._best_selected + self._rest_selected
        self.actual_population = list()
        while len(population_selector) > 1:
            random_member = random.randint(0, len(population_selector)-1)
            pair_a = population_selector.pop(random_member)
            random_member = random.randint(0, len(population_selector)-1)
            pair_b = population_selector.pop(random_member)
            children = self._combine_single_pair(pair_a, pair_b)
            if len(self.actual_population) >= self._population_limit:
                self.actual_population = self.actual_population[:self._population_limit]
                return
            self.actual_population += children
        if len(self.actual_population) < self._population_limit:
            fill_length = self._population_limit - len(self.actual_population)
            self.actual_population += self._rest_fill[:fill_length]

    def _combine_single_pair(self, pair_a, pair_b):
        '''
        Creation of new children
        returns list of Member objects
        '''
        children = list()
        actual_children_count = random.randint(self._min_children,
                                               self._max_children)
        gene_count = self._secret_word_length // 2
        for _ in range(actual_children_count):
            combine_start_pos = random.randint(0, self._secret_word_length - 1)
            gene_positions = [((combine_start_pos + shift) %
                               self._secret_word_length)
                              for shift in range(gene_count)]
            options = [pair_a, pair_b]
            select_a = options.pop(random.randint(0, 1))
            select_b = options.pop()
            child_name_seq = list(select_a.member_name)
            for pos in gene_positions:
                child_name_seq[pos] = select_b.member_name[pos]
                child_name = ''.join(child_name_seq)
            children.append(Member(member_name=child_name, success_score=0.0))
        return children

    def mutation(self):
        '''
        Does the mutation for the whole population
        '''
        true_part = ([True] * self._mutation_probability_coeff)
        false_part = ([False] * (10-self._mutation_probability_coeff))
        mutation_probability_seq = true_part + false_part
        for member in self.actual_population:
            do_mutation = random.choice(mutation_probability_seq)
            if do_mutation:
                cur_name = member.member_name
                member.member_name = self._mutate_single_member(cur_name)

    def _mutate_single_member(self, member_name):
        '''
        mutates a single member
        '''
        member_name_seq = list(member_name)
        for _ in range(self._mutate_element_count):
            modif_position = random.randint(0, self._secret_word_length - 1)
            member_name_seq[modif_position] = random.choice(self._char_set)
        return ''.join(member_name_seq)
