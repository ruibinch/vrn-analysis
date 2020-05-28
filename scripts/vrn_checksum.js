const calcVrnChecksum = (vrn) => {

    // console.log(vrn);
    let padArray = (desiredLength, value) => [...Array(desiredLength).fill('0'), ...value].slice(-desiredLength);

    let alphabet = {
        'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'F': 6, 'G': 7, 'H': 8, 'I': 9, 'J': 10, 'K': 11, 'L': 12, 'M': 13,
        'N': 14, 'O': 15, 'P': 16, 'Q': 17, 'R': 18, 'S': 19, 'T': 20, 'U': 21, 'V': 22, 'W': 23, 'X': 24, 'Y': 25, 'Z': 26,
    };

    let letters = vrn.match(/[A-Za-z]/g);
    let numbers = vrn.match(/[\d]/g);
    // keep last 2 letters
    let lettersSignificant = letters.slice(-2).map(e => alphabet[e.toUpperCase()]);
    // pad numbers to 4 digits
    let numbersSignificant = padArray(4, numbers).map(e => parseInt(e));
    // combine; this array should have 6 digits
    let vrnInNumFormat = [...lettersSignificant, ...numbersSignificant];

    // multiply by 6 fixed numbers - 9, 4, 5, 4, 3, 2
    let sum = vrnInNumFormat.reduce((acc, digit, idx) => {
        if (idx === 0) acc += digit * 9;
        if (idx === 1) acc += digit * 4;
        if (idx === 2) acc += digit * 5;
        if (idx === 3) acc += digit * 4;
        if (idx === 4) acc += digit * 3;
        if (idx === 5) acc += digit * 2;
        return acc;
    }, 0);

    let checksumMapping = 'AZYXUTSRPMLKJHGEDCB';
    return checksumMapping[sum % 19];
}

const letters = ['SKA', 'SKB', 'SKC', 'SKD', 'SKE', 'SKF', 'SKG', 'SKH', 'SKJ', 'SKK', 'SKL'];
const numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 18, 28, 88, 99, 100, 888, 999, 8888];

letters.forEach((letter) => {
    console.log('Series = ' + letter);
    numbers.forEach((number) => {
        const checksum = calcVrnChecksum(letter + number);
        console.log(checksum);
    });
});
