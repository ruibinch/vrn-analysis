from utils import gsheet
    
"""
Helper script to calculate VRN checksum letters.
"""

VRN_LETTERS = [
    'SKA','SKB','SKC','SKD','SKE','SKF','SKG','SKH','SKJ','SKK','SKL','SKM','SKN','SKP','SKQ','SKR','SKS','SKT','SKU','SKV','SKW','SKX','SKZ',
    'SLA','SLB','SLC','SLD','SLE','SLF','SLG','SLH','SLJ','SLK','SLL','SLM','SLN','SLP','SLQ','SLR','SLS','SLT','SLU','SLV','SLW','SLX','SLZ',
    'SMA','SMC','SMD','SME','SMF','SMG','SMH','SMJ','SMK','SML','SMN','SMP','SMQ','SMR','SMS']
VRN_NUMBERS = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 18, 28, 88, 99, 100, 888, 999, 8888]

def _calc_vrn_checksum(vrn: str) -> str:
    """Calculates the checksum letter for the input VRN combinations.
    
    Args:
        vrn: Input VRN, minus the checksum letter
    
    Returns:
        Corresponding checksum letter
    """

    def _multiply(idx, num):
        """Helper function where each of the 6 digits is multiplied with a corresponding fixed number."""
        fixed_nums = [9, 4, 5, 4, 3, 2]
        return num * fixed_nums[idx]

    letters = [c for c in vrn if c.isalpha()]
    numbers = [c for c in vrn if c.isnumeric()]

    # keep last 2 letters
    # convert letters to numeric equivalent
    letters_significant = [ord(letter.upper()) - 64 for letter in letters[-2:]]
    # pad numbers to 4 elements
    numbers_significant = [*[0 for e in range(4 - len(numbers))],
                           *[int(n) for n in numbers]]

    # combine; this array should have 6 elements
    vrn_numeric = [*letters_significant, *numbers_significant]
    vrn_numeric_sum = sum([_multiply(i, n) for i, n in enumerate(vrn_numeric)])

    checksumMapping = 'AZYXUTSRPMLKJHGEDCB'
    return checksumMapping[vrn_numeric_sum % 19]

def run():
    """Runner method.

    The checksum letters are inserted into the "Checksum" worksheet in rows.
    """

    output = []
    # prepare list of lists
    for letter in VRN_LETTERS:
        checksum = [letter]
        for number in VRN_NUMBERS:
            checksum.append(_calc_vrn_checksum(f'{letter}{number}'))
        output.append(checksum)

    # save to "Checksum" worksheet in GSheets
    gsheet.save_to_worksheet(
        '18KGQFVDZ8wgj2pb1ErKh2QXGtF1N2U17GiwRBcXI1TI',
        'Checksum',
        output,
        True)
