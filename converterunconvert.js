function mapToDecimal(numbers) {
    let result = "1"
    for (let i = 0; i < numbers.length - 1; i++) {
        let startLineIndex = numbers.indexOf(i + 1);  
        let endLineIndex = numbers.indexOf(i + 2);
        result += ""+(+(endLineIndex - startLineIndex >= 1))
    }
    return parseInt( result.split('').join(''), 2 );

}

console.log(mapToDecimal([5, 1, 2, 3,4, 6, 7]))

function decimalToMap(number){
    let binary = number.toString(2)
    let array = [1]
    for (let i = 1; i < binary.length; i++) {
        if(binary[i] == 1){
            array.push(i+1)
        } else {
            array.unshift(i+1);
        }
    }
    return array
}

console.log(decimalToMap(123456789))