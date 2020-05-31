const calcVrnChecksum = (vrn) => {

    const padArray = (desiredLength, value) => {
        return [
            ...Array(desiredLength).fill('0'), 
            ...value,
        ].slice(-desiredLength);
    };

    const letters = vrn.match(/[A-Za-z]/g);
    const numbers = vrn.match(/[\d]/g);

    // keep last 2 letters
    // convert letters to numeric equivalent
    const lettersSignificant = letters.slice(-2).map(e => {
        return e.toUpperCase().charCodeAt(0) - 64;
    });
    // pad numbers to 4 elements
    const numbersSignificant = padArray(4, numbers).map(e => parseInt(e));
    
    // combine; this array should have 6 elements
    const vrnNumeric = [...lettersSignificant, ...numbersSignificant];
    // multiply by 6 fixed numbers - 9, 4, 5, 4, 3, 2
    const fixedNums = [9, 4, 5, 4, 3, 2];
    const sum = vrnNumeric.reduce((acc, digit, idx) => {
        acc += digit * fixedNums[idx];
        return acc;
    }, 0);

    const checksumMapping = 'AZYXUTSRPMLKJHGEDCB';
    return checksumMapping[sum % 19];
}
