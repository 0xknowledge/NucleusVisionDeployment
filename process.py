import constants
from web3 import Web3
import csv

def process_airdrop():
  print ('\n\n\nProcessing AirDrop List')
  airdrop_list = [i.strip() for i in open(constants.AIRDROP_FILE).read().split() if i.strip()]
  airdrop_final = []
  error = []
  not_checksum = 0
  duplicate = 0
  for i in airdrop_list:
    if not Web3.isAddress(i):
      error.append(i)
      continue
    if not Web3.isChecksumAddress(i):
      not_checksum += 1
      addr_with_checksum = Web3.toChecksumAddress(i)
    else:
      addr_with_checksum = i
    if i in airdrop_final:
      duplicate += 1
      continue
    else:
      airdrop_final.append(i)

  print ('Processing {} input address.\n{} addresses are invalid.\n{} addresses got corrected for checksum.\n{} addresses were duplicates.\nFinally got {} valid addresses'.format(len(airdrop_list), len(error), not_checksum, duplicate, len(airdrop_final)))

  # for i in error:
  #   print (i)

  return airdrop_final

def process_presale():
  print ('\n\n\nProcessing Presale List')
  rows = [i for i in csv.reader(open('presale.feb23-1800.tsv', 'r'), delimiter='\t')]
  # neglect first row
  rows = rows[1:]
  presale_final = []

  for row in rows:
    addr, tokens, notes = row
    addr = addr.strip()
    if not Web3.isAddress(addr):
      print ('Invalid Address <{}> for {}'.format(addr, notes))
      continue

    if not Web3.isChecksumAddress(addr):
      addr = Web3.toChecksumAddress(addr)

    tokens = int(tokens.replace(',', '').strip())
    presale_final.append([addr, tokens])

  print ('Processed {} input and got {} valid presale allocation with {} total tokens'.format(len(rows), len(presale_final), sum(i[1] for i in presale_final)))

  return presale_final

def process_presale_bonus():
  print ('\n\n\nProcessing Presale List')
  rows = [i for i in csv.reader(open('presale.bonus.feb23-1800.tsv', 'r'), delimiter='\t')]
  # neglect first row
  rows = rows[1:]
  presale_bonus_final = []

  for row in rows:
    addr, tokens, cliff, notes, _, _, _ = row
    addr = addr.strip()
    if not Web3.isAddress(addr):
      print ('Invalid Address <{}> for {}'.format(addr, notes))
      continue

    if not Web3.isChecksumAddress(addr):
      addr = Web3.toChecksumAddress(addr)

    tokens = int(tokens.replace(',', '').strip())
    presale_bonus_final.append([addr, tokens, int(cliff)])

  print ('Processed {} input and got {} valid presale allocation with {} total tokens'.format(len(rows), len(presale_bonus_final), sum(i[1] for i in presale_bonus_final)))

  return presale_bonus_final

def process_advisors():
  print ('\n\n\nProcessing Advisors List')
  rows = [i for i in csv.reader(open('advisors.feb23-1800.tsv', 'r'), delimiter='\t')]
  # neglect first row
  rows = rows[1:]
  advisors_final = []

  for row in rows:
    addr, notes, _, tokens, cliff, duration = row
    addr = addr.strip()
    if not Web3.isAddress(addr):
      print ('Invalid Address <{}> for {}'.format(addr, notes))
      continue

    if not Web3.isChecksumAddress(addr):
      addr = Web3.toChecksumAddress(addr)

    tokens = int(float((tokens.replace(',', '').strip())))
    advisors_final.append([addr, tokens, int(cliff), int(duration)])

  print ('Processed {} input and got {} valid presale allocation with {} total tokens'.format(len(rows), len(advisors_final), sum(i[1] for i in advisors_final)))

  return advisors_final


with open('data.py', 'w') as f:
  value = ',\n'.join(['%r' % i for i in process_presale()])
  f.write('PRESALE = [' + value + ']\n\n')
  value = ',\n'.join(['%r' % i for i in process_presale_bonus()])
  f.write('PRESALE_BONUS = [' + value + ']\n\n')
  value = ',\n'.join(['%r' % i for i in process_advisors()])
  f.write('ADVISORS = [' + value + ']\n\n')
  value = ',\n'.join(['%r' % i for i in process_airdrop()])
  f.write('AIR_DROP = [' + value + ']\n\n')
