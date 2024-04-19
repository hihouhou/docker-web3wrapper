from flask import Flask, request, jsonify
from web3 import Web3
import json

app = Flask(__name__)

web3 = Web3(Web3.HTTPProvider('http://go-callisto:7545'))
contract_address = "0x810059e1406dEDAFd1BdCa4E0137CbA306c0Ce36"
contract_abi = [{"type":"constructor","stateMutability":"nonpayable","inputs":[{"type":"address","name":"_firstUser","internalType":"address"},{"type":"string","name":"_name","internalType":"string"}]},{"type":"event","name":"ChangeStatus","inputs":[{"type":"uint256","name":"_id","internalType":"uint256","indexed":True},{"type":"uint8","name":"_status","internalType":"uint8","indexed":False}],"anonymous":False},{"type":"event","name":"Claim","inputs":[{"type":"address","name":"_sender","internalType":"address","indexed":True},{"type":"uint256","name":"_id","internalType":"uint256","indexed":True},{"type":"uint256","name":"_pay","internalType":"uint256","indexed":False}],"anonymous":False},{"type":"event","name":"CreateProposal","inputs":[{"type":"uint256","name":"_id","internalType":"uint256","indexed":True},{"type":"uint256","name":"_reward","internalType":"uint256","indexed":False}],"anonymous":False},{"type":"event","name":"Vote","inputs":[{"type":"address","name":"_sender","internalType":"address","indexed":True},{"type":"uint256","name":"_id","internalType":"uint256","indexed":True},{"type":"bool","name":"_answer","internalType":"bool","indexed":False}],"anonymous":False},{"type":"function","stateMutability":"nonpayable","outputs":[],"name":"addUserInDAO","inputs":[{"type":"address","name":"_user","internalType":"address"},{"type":"string","name":"_name","internalType":"string"}]},{"type":"function","stateMutability":"view","outputs":[{"type":"bool","name":"","internalType":"bool"}],"name":"checkClaim","inputs":[{"type":"uint256","name":"_id","internalType":"uint256"},{"type":"address","name":"_user","internalType":"address"}]},{"type":"function","stateMutability":"nonpayable","outputs":[],"name":"claim","inputs":[{"type":"uint256","name":"_id","internalType":"uint256"}]},{"type":"function","stateMutability":"payable","outputs":[],"name":"createProposal","inputs":[{"type":"address","name":"_contract","internalType":"address"},{"type":"bytes","name":"_data","internalType":"bytes"},{"type":"string","name":"_comment","internalType":"string"}]},{"type":"function","stateMutability":"nonpayable","outputs":[],"name":"delUserInDAO","inputs":[{"type":"address","name":"_user","internalType":"address"}]},{"type":"function","stateMutability":"nonpayable","outputs":[],"name":"execute","inputs":[{"type":"uint256","name":"_id","internalType":"uint256"}]},{"type":"function","stateMutability":"view","outputs":[{"type":"uint256","name":"","internalType":"uint256"}],"name":"expire_period","inputs":[]},{"type":"function","stateMutability":"view","outputs":[{"type":"uint256[]","name":"","internalType":"uint256[]"},{"type":"bool[]","name":"","internalType":"bool[]"}],"name":"getClaimList","inputs":[{"type":"address","name":"_user","internalType":"address"},{"type":"uint256","name":"_start_ID","internalType":"uint256"},{"type":"uint256","name":"_amount","internalType":"uint256"}]},{"type":"function","stateMutability":"view","outputs":[{"type":"tuple","name":"","internalType":"struct GovernanceDAO.ProposalData","components":[{"type":"uint256","name":"id","internalType":"uint256"},{"type":"uint256","name":"time","internalType":"uint256"},{"type":"uint256","name":"reward","internalType":"uint256"},{"type":"uint256","name":"deadLine","internalType":"uint256"},{"type":"address","name":"owner","internalType":"address"},{"type":"uint8","name":"status","internalType":"uint8"},{"type":"string","name":"comment","internalType":"string"},{"type":"address[]","name":"vocesYes","internalType":"address[]"},{"type":"address[]","name":"vocesNo","internalType":"address[]"},{"type":"address","name":"to","internalType":"address"},{"type":"bytes","name":"data","internalType":"bytes"}]}],"name":"getProposal","inputs":[{"type":"uint256","name":"_id","internalType":"uint256"}]},{"type":"function","stateMutability":"view","outputs":[{"type":"tuple[]","name":"","internalType":"struct GovernanceDAO.ProposalData[]","components":[{"type":"uint256","name":"id","internalType":"uint256"},{"type":"uint256","name":"time","internalType":"uint256"},{"type":"uint256","name":"reward","internalType":"uint256"},{"type":"uint256","name":"deadLine","internalType":"uint256"},{"type":"address","name":"owner","internalType":"address"},{"type":"uint8","name":"status","internalType":"uint8"},{"type":"string","name":"comment","internalType":"string"},{"type":"address[]","name":"vocesYes","internalType":"address[]"},{"type":"address[]","name":"vocesNo","internalType":"address[]"},{"type":"address","name":"to","internalType":"address"},{"type":"bytes","name":"data","internalType":"bytes"}]}],"name":"getProposalsList","inputs":[{"type":"uint256","name":"_start_ID","internalType":"uint256"},{"type":"uint256","name":"_amount","internalType":"uint256"}]},{"type":"function","stateMutability":"view","outputs":[{"type":"tuple","name":"","internalType":"struct GovernanceDAO.UserData","components":[{"type":"uint256","name":"index","internalType":"uint256"},{"type":"uint256","name":"votes","internalType":"uint256"},{"type":"uint256","name":"entered","internalType":"uint256"},{"type":"address","name":"userAddr","internalType":"address"},{"type":"string","name":"name","internalType":"string"}]}],"name":"getUser","inputs":[{"type":"address","name":"_user","internalType":"address"}]},{"type":"function","stateMutability":"view","outputs":[{"type":"tuple[]","name":"","internalType":"struct GovernanceDAO.UserData[]","components":[{"type":"uint256","name":"index","internalType":"uint256"},{"type":"uint256","name":"votes","internalType":"uint256"},{"type":"uint256","name":"entered","internalType":"uint256"},{"type":"address","name":"userAddr","internalType":"address"},{"type":"string","name":"name","internalType":"string"}]}],"name":"getUsersList","inputs":[{"type":"uint256","name":"_start_index","internalType":"uint256"},{"type":"uint256","name":"_amount","internalType":"uint256"}]},{"type":"function","stateMutability":"view","outputs":[{"type":"uint256","name":"","internalType":"uint256"}],"name":"min_payment_DAO","inputs":[]},{"type":"function","stateMutability":"view","outputs":[{"type":"uint256","name":"","internalType":"uint256"}],"name":"min_payment_other","inputs":[]},{"type":"function","stateMutability":"nonpayable","outputs":[],"name":"setExpirePeriod","inputs":[{"type":"uint256","name":"_period","internalType":"uint256"}]},{"type":"function","stateMutability":"nonpayable","outputs":[],"name":"setMinPayments","inputs":[{"type":"uint256","name":"_min_payment_DAO","internalType":"uint256"},{"type":"uint256","name":"_min_payment_other","internalType":"uint256"}]},{"type":"function","stateMutability":"view","outputs":[{"type":"uint256","name":"","internalType":"uint256"}],"name":"total_close_voting","inputs":[]},{"type":"function","stateMutability":"view","outputs":[{"type":"uint256","name":"","internalType":"uint256"}],"name":"total_user","inputs":[]},{"type":"function","stateMutability":"view","outputs":[{"type":"uint256","name":"","internalType":"uint256"}],"name":"total_voting","inputs":[]},{"type":"function","stateMutability":"nonpayable","outputs":[],"name":"vote","inputs":[{"type":"uint256","name":"_id","internalType":"uint256"},{"type":"bool","name":"_answer","internalType":"bool"}]}]
contract = web3.eth.contract(address=contract_address, abi=contract_abi)

# Exemple de fonction pour /dao/getproposal
@app.route('/dao/getproposal')
def get_proposal():
    proposal_id = int(request.args.get('proposal_id', default=0))  # Défaut à 10 si non spécifié dans la requête

    # Appeler la fonction sur le contrat
    #claim_list = contract.functions.getClaimList(user_address, status, limit).call()
    # Afficher les résultats
    #print("Liste des réclamations:", claim_list)
    # Appeler la fonction sur le contrat
    claim_list = contract.functions.getProposal(proposal_id).call()
    # Afficher les résultats
    #print("Liste des réclamations:", claim_list)
    json_data = json.dumps({
    "uint256": claim_list[0],
    "bool": claim_list[1],
    "reward": claim_list[2],
    "deadline": claim_list[3],
    "owner_address": claim_list[4],
    "status": claim_list[5],
    "comment": claim_list[6],
    "voces_yes": claim_list[7],
    "voces_no": claim_list[8],
    "to_address": claim_list[9],
    "claim_list": claim_list[10].hex()  # Convertir bytes en chaîne hexadécimale
    })
    return json_data
    return claim_list


@app.route('/dao/getclaimlist')
def getclaimlist():
    address = request.args.get('address', default='0x0')  # Défaut à 10 si non spécifié dans la requête
    start = int(request.args.get('start', default=0))  # Défaut à 10 si non spécifié dans la requête
    limit = int(request.args.get('limit', default=0))  # Défaut à 10 si non spécifié dans la requête

    
    
    # Appeler la fonction sur le contrat
    claim_list = contract.functions.getClaimList(address, start, limit).call()
    json_data = json.dumps({
    "uint256": claim_list[0],
    "bool": claim_list[1]
    })
    return json_data

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

