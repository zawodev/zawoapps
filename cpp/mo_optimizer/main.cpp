#include <iostream>
#include <vector>
#include <ctime>
#include <cstdlib>

using namespace std;

const int POPULATION_SIZE = 1000;
const int GENOME_LENGTH = 1024;
const double MUTATION_RATE = 0.01;
const int MAX_GENERATIONS = 30;
const int NUM_IDEAL_SOLUTIONS = 20; // liczba idealnych rozwiązań dla każdego evaluatora
const int SEED = 420; // stały seed

struct Individual {
    vector<int> genome;
    double fitness1;
    double fitness2;
    double fitness3;
};

class FitnessEvaluator {
public:
    FitnessEvaluator(int seed, int num_solutions) {
        srand(seed);
        for (int i = 0; i < num_solutions; ++i) {
            ideal_solutions.push_back(generate_ideal_solution());
        }
    }

    double evaluate(const vector<int>& genome) {
        double max_fitness = 0.0;
        for (const auto& ideal : ideal_solutions) {
            double fitness = calculate_fitness(genome, ideal);
            if (fitness > max_fitness) {
                max_fitness = fitness;
            }
        }
        return max_fitness;
    }

private:
    vector<vector<int>> ideal_solutions;

    vector<int> generate_ideal_solution() {
        vector<int> ideal_solution(GENOME_LENGTH);
        for (int i = 0; i < GENOME_LENGTH; ++i) {
            ideal_solution[i] = rand() % 2; // losowy bit
        }
        return ideal_solution;
    }

    double calculate_fitness(const vector<int>& genome, const vector<int>& ideal) {
        double fitness = 1.0;
        for (size_t i = 0; i < genome.size(); ++i) {
            if (genome[i] != ideal[i]) {
                fitness -= 1.0 / GENOME_LENGTH;
            }
        }
        return fitness < 0 ? 0 : fitness;
    }
};

// Tworzenie evaluatorów z różnymi seedami
FitnessEvaluator evaluator1(SEED, NUM_IDEAL_SOLUTIONS);
FitnessEvaluator evaluator2(SEED + 1, NUM_IDEAL_SOLUTIONS);
FitnessEvaluator evaluator3(SEED + 2, NUM_IDEAL_SOLUTIONS);

vector<Individual> initialize_population() {
    vector<Individual> population;
    for (int i = 0; i < POPULATION_SIZE; ++i) {
        Individual ind;
        ind.genome = vector<int>(GENOME_LENGTH);
        for (int j = 0; j < GENOME_LENGTH; ++j) {
            ind.genome[j] = rand() % 2; // losowy bit
        }
        population.push_back(ind);
    }
    return population;
}

void evaluate_population(vector<Individual>& population) {
    for (auto& ind : population) {
        ind.fitness1 = evaluator1.evaluate(ind.genome);
        ind.fitness2 = evaluator2.evaluate(ind.genome);
        ind.fitness3 = evaluator3.evaluate(ind.genome);
    }
}

bool dominates(const Individual& a, const Individual& b) {
    return (a.fitness1 > b.fitness1 && a.fitness2 >= b.fitness2 && a.fitness3 >= b.fitness3) ||
           (a.fitness1 >= b.fitness1 && a.fitness2 > b.fitness2 && a.fitness3 >= b.fitness3) ||
           (a.fitness1 >= b.fitness1 && a.fitness2 >= b.fitness2 && a.fitness3 > b.fitness3);
}

vector<Individual> select_pareto_front(const vector<Individual>& population) {
    vector<Individual> pareto_front;
    for (const auto& ind : population) {
        bool is_dominated = false;
        for (const auto& other : population) {
            if (dominates(other, ind)) {
                is_dominated = true;
                break;
            }
        }
        if (!is_dominated) {
            pareto_front.push_back(ind);
        }
    }
    return pareto_front;
}

Individual crossover(const Individual& parent1, const Individual& parent2) {
    Individual offspring;
    offspring.genome = vector<int>(GENOME_LENGTH);
    int crossover_point = rand() % GENOME_LENGTH;
    for (int i = 0; i < GENOME_LENGTH; ++i) {
        if (i < crossover_point) {
            offspring.genome[i] = parent1.genome[i];
        } else {
            offspring.genome[i] = parent2.genome[i];
        }
    }
    return offspring;
}

void mutate(Individual& ind) {
    for (int i = 0; i < GENOME_LENGTH; ++i) {
        if ((rand() / static_cast<double>(RAND_MAX)) < MUTATION_RATE) {
            ind.genome[i] = 1 - ind.genome[i]; // zamiana 0 na 1 lub 1 na 0
        }
    }
}

int main() {
    srand(time(0));
    vector<Individual> population = initialize_population();
    evaluate_population(population);

    for (int generation = 0; generation < MAX_GENERATIONS; ++generation) {
        vector<Individual> new_population;

        // Selekcja frontu Pareto
        vector<Individual> pareto_front = select_pareto_front(population);
        cout << "Generacja: " << generation << " | Front Pareto: " << pareto_front.size() << endl;

        while (new_population.size() < POPULATION_SIZE) {
            // Turniej selekcyjny
            Individual parent1 = pareto_front[rand() % pareto_front.size()];
            Individual parent2 = pareto_front[rand() % pareto_front.size()];

            // Krzyżowanie
            Individual offspring = crossover(parent1, parent2);

            // Mutacja
            mutate(offspring);

            // Ocena potomka
            offspring.fitness1 = evaluator1.evaluate(offspring.genome);
            offspring.fitness2 = evaluator2.evaluate(offspring.genome);
            offspring.fitness3 = evaluator3.evaluate(offspring.genome);

            new_population.push_back(offspring);
        }

        population = new_population;
        evaluate_population(population);
    }

    // Wyświetlenie ostatecznego frontu Pareto
    vector<Individual> final_pareto_front = select_pareto_front(population);
    cout << "Ostateczny front Pareto:" << endl;
    for (const auto& ind : final_pareto_front) {
        cout << "Genome: ";
        for (int gene : ind.genome) {
            cout << gene;
        }
        cout << " | F1: " << ind.fitness1 << " | F2: " << ind.fitness2 << " | F3: " << ind.fitness3 << endl;
    }

    return 0;
}
