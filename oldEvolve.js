const MUTATION_RANGE = [1, 7];
const MAX_ITERATIONS = 5000;
const MAX_TESTS = 31;
let currentRules = [1];
let Mutation1 = [1];
let Mutation2 = [1];
let lowestErrorScore = 3000000;
let errorSum1;
let errorSum2;
let bestRuleSet = [];
let best = 0
for (let i = 0; i < MAX_ITERATIONS; i++) {
    mutate(Mutation1);
    mutate(Mutation2);

    // Ensure Mutation1 and Mutation2 are not producing the same output for all tests
    errorSum1 = calculateErrorSum(Mutation1);
    errorSum2 = calculateErrorSum(Mutation2);

    if (errorSum1 < lowestErrorScore) {
        best = 1
        lowestErrorScore = errorSum1;
        bestRuleSet = [...Mutation1];
    }
    if (errorSum2 < lowestErrorScore) {
        best = 0
        lowestErrorScore = errorSum2;
        bestRuleSet = [...Mutation2];
    }

    let isMutation1Repeated = isMutationRepeated(Mutation1);
    let isMutation2Repeated = isMutationRepeated(Mutation2);

    if (isMutation1Repeated && !isMutation2Repeated) {
        console.log("Mutation 2 was favored (Mutation 1 repeated output)", errorSum1, errorSum2);
        best = 0
        currentRules = [...Mutation2];
        Mutation1 = [...Mutation2];
    } else if (isMutation2Repeated && !isMutation1Repeated) {
        best = 1
        console.log("Mutation 1 was favored (Mutation 2 repeated output)", errorSum1, errorSum2);
        currentRules = [...Mutation1];
        Mutation2 = [...Mutation1];
    } else {
        if (errorSum1 < errorSum2) {
            best = 1
            currentRules = [...Mutation1];
            Mutation2 = [...Mutation1];
            console.log("Mutation 1 was favored", errorSum1, errorSum2);
        } else {
            best = 0
            currentRules = [...Mutation2];
            Mutation1 = [...Mutation2];
            console.log("Mutation 2 was favored", errorSum1, errorSum2);
        }
    }
}
if(best){
    console.log("Mutation 1 favored most recently",errorSum1,Mutation1.join(','))
} else{
    console.log("Mutation 2 favored most recently",errorSum2,Mutation2.join(','))
}
console.log("Best ruleset of all time:", lowestErrorScore, bestRuleSet.join(','));

// Helper functions:

function mutate(rules) {
    const mutationType = Math.round(Math.random() * (3 - 1) + 1);  // Fixed the typo here
    const newValue = Math.floor(Math.random() * (MUTATION_RANGE[1] - MUTATION_RANGE[0] + 1) + MUTATION_RANGE[0]);
    switch (mutationType) {
        case 1: 
            rules.push(newValue);
            break;
        case 2:
            const randomIndex = Math.floor(Math.random() * rules.length);
            rules[randomIndex] = newValue;
            break;
        case 3:
            if(rules.length > 5){
                rules.pop()
            }
        break;
    }
}

function calculateErrorSum(mutation) {
    let errorSum = 0;
    for (let j = 1; j < MAX_TESTS; j++) {
        let num = decimalToMap(j);
        let target = (Math.floor(Math.floor((Math.sin(j)+1)*10)*0.2))
        ApplyRules(num, mutation);
        errorSum += Math.abs(mapToDecimal(num) - target);
    }
    return errorSum;
}

function isMutationRepeated(mutation) {
    let previousOutput = null;
    let repeated = true;

    for (let j = 1; j < MAX_TESTS; j++) {
        let num = decimalToMap(j);
        ApplyRules(num, mutation);
        if (previousOutput && JSON.stringify(previousOutput) !== JSON.stringify(num)) {
            repeated = false;
        }
        previousOutput = [...num];
    }

    return repeated;
}

function ApplyRules(array, rules) {
    for (let rule of rules) {
        switch (rule) {
            case 1:
                if (array[array.length - 1] < array[0]) {
                    swapDigits(array, 0); // Swap digits at position 0
                }
                break;
            case 2:
                if (array[array.length - 1] < array[0]) {
                    swapDigits(array, 1); // Swap digits at position 1
                }
                break;
            case 3:
                removeLargestDigit(array); // Remove the largest digit
                break;
            case 4:
                addNextDigit(array, 0); // Add next digit with offset 0
                break;
            case 5:
                addNextDigit(array, 1); // Add next digit with offset 1
                break;
            case 6:
            if(array.length > 3){
              array.length = 0
              array.push(1)
            }
            break;
			case 7:
            let arraylength = array.length
            for (let j = 1; j < arraylength; j++) {
              array.push(arraylength+j)              			
            }     
            break;
        }
    }
}

function mapToDecimal(numbers) {
    return numbers.length
}

function decimalToMap(number) {
    let array = []
    for (let i = 1; i < number+1; i++) {
        array.push(i)
    }
    return array;
}

function removeLargestDigit(array) {
    const largestNum = Math.max(...array);
    const index = array.indexOf(largestNum);
    if (index > -1) array.splice(index, 1);
}

function addNextDigit(array, side) {
    const nextBiggestNum = Math.max(...array) + 1;
    side ? array.push(nextBiggestNum) : array.unshift(nextBiggestNum);
}

function swapDigits(array, side) {
    const arrayLength = array.length - 1;
    if (side === 0) {
        [array[arrayLength - 1], array[arrayLength]] = [array[arrayLength], array[arrayLength - 1]];
    } else {
        [array[0], array[1]] = [array[1], array[0]];
    }
}

