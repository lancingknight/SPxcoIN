# Minimal replica in a distributed database 

	Version 1.0	
	Ling Wu
	November 30, 2017

## Abstract
	A crypto-currency protocol to minimize the distributed database and simplify verification procedures.  
	We created a protocol to enable large number of transactions at low cost or no cost. We also deviced 
	a protocol for listing and trading of standardized contracts within the system.

## Minimal Replica
	
	Let Si(t) be the state (or balance) of an account i with a public key Pi . We claim that a minimal 
	replica of a distributed database that each node would only need to include set of entries {Ht}, as 
	long as there exists a collision resistant hash function such that
					 Ht =  Hash({Si(t) ,  Pi})    
	At time v>t, assume i has no transactions between t and v,  as long as i can present state Si(t) and 
	its signature that can reproduce an entry Ht in the Minimal Replica set {Ht}, its will be able to 
	convince all nodes that its ownership and state of the account i. At time v, suppose i wants to initiate 
	a transaction X(v,i,j)  with account j, new state of account i can be calculated with the state transition 
	function F  
					Si(v)= F(Si(t), X(v,i,j))
	Likewise when the account j accepts the transaction, it will present Sj(t) and its signature that can 
	recreate another entry Ht′ in {Ht} 
	And the database will be updated by deleting two old entries Ht and Ht′, and inserting two new entries 
					Hv = Hash({Si(v), Pi})  
					Hv′ = Hash({Sj(v), Pj})   
	The above described minimal database will unload burden of storing the tansactions and account balances 
	off all the users,  except for the owner, who would have all the incentives to keep track of its own account 
	balances. If N is number of accounts, the storage of the minimal replica would be O(N), and the speed of 
	verification the state of an account will be O(logN). 
	It would create a new ecosystem that would be both economical and scalable. Every node keeps its own account 
	balance is a de-facto sharding of the database by accounts. Moreover, if the owner would prefer to have its 
	account balance backed up by others, it may pay some nodes to do so and competition among these nodes would 
	drive down the cost. It may also join a small pool of nodes that shares the responsibility and costs. As these 
	backups are easily verifiable by the Minimal Replica, they will be immune to falsification and non-essential 
	to the viability of the system as long as each account keeps a record of its last account balances.
	
## Consensus procedure for simple transactions
	
	To make the Minimal Replica described above become feasible, it would require a protocol to form a consensus 
	on how the database is updated.  
	
	We would still use the proof-of-work to form a block-chain, thus time-stamping the  transactions. However, 
	instead of letting every miner work on the same set of transactions, we would want them to work in parallel 
	on subsets of the transactions. We would want non-miners to share the calculation work for the verifications, 
	thus lower the transaction costs. 
	
	Suppose all transactions to be processed are grouped by previous blocks into arrays with prespecified 2^n number 
	of transactions in each array. 
	For each array, a merekle tree with the transactions in the arrays as it leaf nodes will be created. The minimal 
	calculation work includes
		a.  verifying upto 2n+1 number of account ownerships and states
		b.  2^n+1 number of hash values as entries to be inserted in the database
		c.  2^n-1 number of hash values to build a Merkle tree
		d. In order to verify the consistancy of the a Minimal Replica, root hash of the Minimal Replica needs to 
		be recalculated and included in the block header  
		e. proof-of-work to link a new block to the Blockchain
		
	There is a dynamically defined M(t) number of pools where the arrays are allocated to.  M(t) was updated by last 
	block in the Blockchain at t. 
	
	At time t<s, a new candidate transaction X(t,i, j) is broadcasted by account i, after i obtained the approval of j. 
	However, in order for the transaction to be processed, it needs to contribute to the system first by solving for the 
	exsiting transactions, so it will at the same time broadcast 
		a. last observed block time t, thus could observe a rule* to work in only one specified pool M(t, i) 
		of M(t) pools 
		b. choose only one array Ai in the pool and solve a nonce in order to gain the right to work on the array. 
		c. Verify at least R transactions and their related account balances in the array.
		d. Sign its own transaction ID in each of the transactions it verified.
	
	If its processing speed and bandwidth is fast enough, it may also choose to work as a miner instead. 
	A miner will 
		a. solve the nonce from the last block and find an array with all transactions being signed by at least one 
		different candidate transaction ID. When number of the pools significantly increases, the miner may allow to 
		includes more arrays into the block. 
		1) If disagreement of verifications exists, need to re-verify the transaction.   
		2) Update the account info S(t) by including all the transactions from time t to the last block time it observed.  
		3) Form a Merkle tree from the array, each leaf node may include up to Z number of candidate transaction IDs as 
		verifiers, but each candidate transaction ID can only be included once.
		4) recalculate the root hash or a updated Minimal Replica
		5) Include root hash in the block header and link it to the last block 
	
	If, in very rare cases, two miners published two valid blocks at exactly the same time, one with the most number of 
	candidate transaction IDs will be followed by other miners. 
	
	As a block is published, the miner will arrange all the candidate transaction IDs from this block into a sequencial 
	order, and divide them into arrays with each array includes 2n number of transactions. The miner will put the arrays 
	in other pools that have less than pre-specified Z number of arrays. If all the other pools have more or equal than 
	Z number of arrays, a new pool will be created to put these arrays.  
	A pool without any array will be deleted. Thus number of pools will be updated to M(t+1), which dynamically accomendates 
	the total number of transactions. 
	
	If there left some candidate transaction IDs  that are not enough to form an array, the miner will push them into a queue. 
	The miner will also need to pull the candidate transaction IDs out of the queue if the queue becomes long enough to form 
	an array.
	
	As each account contributes to the processing of other transactions in order for its transaction to be put into processing, 
	no fees will be charged for these transactions.      
	
	However, before consensus is reached, all the physical nodes has to store not only the changes to the minimal replica, 
	but also include all the transactional information. We suggest a grace period G that forks can be allowed to exist at 
	block s in the Blockchain until being voted on by a Quorum, which is a combination of votes from users, developers,  
	stake-holder and processing power (the Quorum will be discussed in our governance section). 
	Quorum could also be called on by any challenger to a block during its grace period with a fee. 
	A series of quorums could be called by increasing fees and numbers in the qurorum. 
	
	Once consensus is reached at the quorum(s) or the block is left unchallenged before the grace period ends, 
	a block time spot t before s can be found that all blocks before it are no longer related to any unprocessed 
	orders. A user could decide to delete all transactional information and keep only the headers in BlockChain before 
	and including t and replace the deleted transactional infomation by an updated Minimal Replica {Ht} in its own database. 
	
## Order submission and order matching
	
	If orders are placed like a candidate transaction and a miner picked up the order and timestamp it into an array, 
	it would make exchanging tokens of any contracts possible. 
	In our protocol, types of standardized contracts will be programmed and audited by key developers and approved by a 
	quorum. We prefer standardized contract as its development will be more economical and monitoring and governance 
	will be easier and more transparent. 
	Upon approval by the quorum, various tokens using the approved standardized contracts can be issued.  
	
### Issuance
	
	Any account can create a Listing Order with an untaken token ticker and issuance size and going to the processing 
	like a simple transactions. It will be pick up by a miner and post it on an Auction board for a X block time. 
	The issuer should pay an amount posting fee that is in proportion to the block time on the issuance board. 
	During the period, a Dutch auction will be carried, that any accounts can bid to the issuances with a price 
	and an amount by create a Subscription Order and pick up by the minor to insert it on the Auction board. 
	To limit the number of low-price bids, a lowest price can be specified by the issuer. Miners in these period, 
	collect the fee and verify the Subscription Orders. At the end of the X block time, the miner at the time will 
	rank all bids and determine the highest price at which the total offering can be sold. It will publish these 
	transactions, i.e. the issuer receives the proceeds and bidders receive the tokens, into the transaction pools to 
	be processed. As these transactions do not contribute to the processing other transactions, they need to pay a 
	fee to be collected by the miner who links the block.
	
### Order Trading
	
	A Direct Trading between two specified accounts can be carried like a simple transaction in the system for free. 
	
	A Trading Order (buying or selling a token), however, needs to be matched to a counter-party, thus carrying extra 
	work and storage and a order fee will be paid to the system. Two queues will be established for a token. The order 
	also need to process transactions in a block. Once the block is linked, the miner will insert the orders into buy-order 
	or sell-order queue.  Limit order with higher (lower) price will have higher priority in the buyer-order (sell-order) 
	queue.  Market Order will be inserted before the limited orders which cannot cross the bid-ask price and after the 
	existing market orders. Then the miner will pull the orders from the beginning of the queue and match the order by 
	inserting three simple transactions into a transaction array: 
	1)  Buyer receives the tokens and seller receives fund. 
	2) Buyer pays the order fee to the miner 
	3) seller pays the order fee to the Developer Pool. Developer Pool will be allocated to developers following governance 
	procedure that reward developers in the long-run by encouraging innovations and sustainability. 
	If an order size is too big, it may delay the price discovery process. A size limit of the orders need to be specified . 
	Orders with size larger than the limit need to be carried out at Block Trading.
	Orders may be partially matched. The unmatched partial order will remain in the order queues. 
	
	Cancelling order instructions can be processed like a candidate transaction and picked up by the miner. If the order 
	has not been matched, the miner will pull the order from the queue and inserting a transaction to the transaction array 
	that pays the order fee to the miner. There will be a expiration time for the order, when the unmatched order will expire 
	and fees been collected. To keep the order beyond expiration, the order need to include a listing fee in proportion to the 
	time.
	
### Transfer of portfolio
	
	As long as a portfolio of assets is in an account, the transfer of the portfolio between specified counterparties would 
	be as trivial as a Direct Trading with a single asset being replaced by a set of assets in the transaction. 
	It would be free. 
	
### Block Trading and auctions
	
	A process similar to issuance board can be called. The difference is that a seller of a large block of assets will need 
	to be verified in procession of the tokens before a Dutch auction being carried out. A buyer of intention to buy a block 
	can also initiate a  block trading by given an specified maximum price and intended amount and verification of procession 
	of the fund. Listing fees and transaction will be collected by the miners. 
	
## Safety	
	
### Free-riders
	
	It is true that accounts may free-ride the system by issuing a verification, following earlier verifiers without actually 
	doing the calculations. We would implement an Asynchronous lockstep protocol which will limited the free-riding behaviors. 
	A verifier needs to pre-announce its last observed block time and the array it is working on before announcing its 
	verifications within a limited period, or will be ignored by miners in the pool. The first verifier of an transaction, 
	however, will not need a pre-announcement, so gives verifier an incentive to work on the unverified transactions first.
	Moreover, as there are limited number of verifiers can be included, so there are incentives to pick the nodes that no or 
	few have processed. In order to reduce the chance of following the wrong verifiers and being left out, there is incentives 
	to work out the verification by themselves.
	
### Sybil attack
	The system has significant redundancy in terms of database being replicated to all nodes, transaction processing at 
	parallel pools, multiple verifiers in each transactions and large number of miners competing to link blocks.  
	If 1/3 of the physical nodes are Sybil nodes that are not able to work, as the candidate transactions are randomly 
	assigned to transaction pools, suppose physical nodes generate similar frequency of transactions, while there may 
	be short-term reduction in the processing power due to fewer candidate transactions, as number of transaction pools
	reduces, the transaction speed of each pool will recover. 
	
	If the Sybil nodes try to write false transactions into the database.  Suppose no Sybil nodes are miners, before any 
	false transactions can be put into the array, they need to help verifying the existing transactions, where they must 
	do the work truthfully, otherwise it would be difficult for their transactions to be selected by the miners into arrays. 
	
	When their false transaction is included into arrays, there is a still a low chance that no discrepancy would occur 
	among its verification results. For no discrepancy to happen, all honest verifiers cannot choose the false transaction 
	from the array.  For example, if each truthful account randomly choose 6 from 64 transactions in an array, while Sybil 
	accounts choose the false transaction, there is slightly higher than 2% chance that no discrepancy will show. 
	If we increase the minimal number of choices to 10 transactions, the probability dropped to less than 0.1%. 
	
	Suppose a Sybil node is the miner and publishes the false transaction, the other miners could still identifiy the 
	problem by creating a fork away from the block. Moreover, during the grace period, anyone identifies the problem could 
	still create a challege to call the quorum to verify the block again. 
	
	Suppose Sybil nodes try to publish a large number of invalid transactions to overwhelm the system, the problem will be 
	limited as verifications of other transactions and nonce need to be calculated before the invalid transcations to 
	be put into arrays. For non-simple transactions, there will also be fees paid for each orders or transactions. 
	It woud be computationally and financially expensive to carry on a prolonged attack.
	 
## Privacy
	
	It will be impossible get account information from Minimal Replica along. As account keeps tracking its own account 
	balances, it can choose to have various level of privacy. It can choose to have only  one private key and public key 
	and thus have its account traceable. It may also choose to have a scheme that produces multiple public keys, each of 
	which could receive and pay a fund or asset for only once, which are less likely to be traced. For example
		Public key = hash( F(Private, Last Block Time, Transaction Number)) 
	Is a dynamic public key that changes with block time and transactions, thus would be difficult to able to  trace, as 
	there are infinitely many possible schemes like this.   
	Multiple public keys may also limit the number of consolidations during the verification procedures when multiple 
	transactions happen in multiple period since the announcement of transactions.   
	We would also implement a ring-signature verification module, which is more impossible to trace. The rings of accounts 
	that create the ring-signature could also coincide with the pool that shares the responsibility to backup account balances.   
	
## Governance 
	
	We would like to form a voting system that represents the interests of users, stake holders, processing power and 
	developers. The representatives of the developers will be elected for a specific period by accounts with balances 
	exceeding certain requirement at the beginning of the period.  At a quorum for period from t to s, will be selected 
	from four groups
	1) accounts with verified transitions exceed certain level during the period 
	2) miners in a specified period  
	3) accounts with holding value exceeding certain level at time t and 
	4) representatives of the developers. 
	Each group would have 1/4 of the voting power.  
	
## Economy
	
	Mild inflation is beneficial for the general economy in the system, but sudden increase or decrease in prices of the 
	standard contracts due to change in velocity of money may be harmful for the system. Our design of dynamically changing
	number of pools and number of arrays to be included in a block could absorb some of the impact from velocity of money, 
	which enable us to apply a gradual increase supply of money that is in proportion to the increase in value of the listed 
	tokens. The increase in supply of money and its distribution will be periodically voted by a quorum. 

