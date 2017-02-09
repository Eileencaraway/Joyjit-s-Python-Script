
from scipy import *
import matplotlib.pyplot as plt
import numpy.random as nr
import numpy.linalg as nl
import pickle
with open("wikilinks.pickle","rb") as f:
    titles,links= pickle.load(f)
with open("physicists.pickle","rb") as k:
    physicists=pickle.load(k)



def pagerank_demo(d=0.1):
    #generate a markov chain
    N=10000;d=0.1;M=6
    T=linspace(0,N,N)
    Markov_chain= zeros(len(T))
    #to store the imformation of times the page is visited after each time steps
    PageRank=zeros((N,M))
    p=zeros(M)
    link= array([[1,3],[0,2],[1],[0,1,4],[1],[2]])
    Markov_chain[0]=nr.random_integers(0,5)
    Markov_now=Markov_chain[0]

    for i in range(len(T)):
        Markov_chain[i]=Markov_now
        a=nr.uniform()
        if a<1-d:
            Markov_now=nr.random_integers(0,5)
        elif a>=1-d:
            Markov_now=nr.choice(link[Markov_now])
        for j in range(M):
            if Markov_now==j:
                p[j]+=1
        PageRank[i]=p/(i+1)

    #exact PageRank can be compute like solve eigenvector problem
    #but this method is not suitable for large number of pages
    #from the rules, we can construct the transition matrix
    MatrixMM=zeros((M,M))
    B=zeros(M)
    for i in range(M):
        MatrixMM[i,i]=-1
        B[i]=-0.15
    MatrixMM[1:4,0]=0.05
    MatrixMM[0,1]=0.05
    MatrixMM[0:2,3]=1/30
    MatrixMM[4,3]=1/30
    MatrixMM[1,4]=0.1
    MatrixMM[1:3,5]=0.1
    #print(MatrixMM)
    x=nl.solve(MatrixMM,B)
    #print(x)
    for i in range(M):
        plt.subplot(3,2,i+1)
        plt.plot(T,PageRank[:,i],label='%x'%i)
        plt.axhline(y=x[i],xmin=0,xmax=N)
        plt.xlabel('timesteps_T')
        plt.ylabel('percentage')
        plt.title(x[i])
        plt.legend()


    plt.show()

#pagerank_demo()

def MarkovChain(TN,link):
    Markov_chain= zeros(TN)
    M=len(titles)
    d=0.1
    Markov_now=nr.random_integers(0,M-1)
    
    p=zeros(M)
    PageRank=zeros(M)
    for i in range(TN):
        Markov_chain[i]=Markov_now
        a=nr.uniform()
        if a>=1-d:
            #there are some pages cannot link to other pages 
            if len(links[Markov_now])!=0: 
                Markov_now=nr.choice(links[Markov_now])
        else:
            Markov_now=nr.random_integers(0,M-1)
        for j in range(M):
            if Markov_now==j:
                p[j]+=1
    for j in range(M):
        PageRank[j]=p[j]/(TN)
    
    return Markov_chain,PageRank

def pagerank_wikipedia_demo(d=0.1):
    T=100000
    A,PR=MarkovChain(T,links)
    # the probability of each page is visited is stored in PR
    # rearange PR and Title from large to small
    idx=argsort(PR)
    count=0
    #print the top 200 wikipedia pages
    #for i in range(200):
        #print('%d. %s'%(1+i,titles[idx[N-1-i]]))
    #print the top 20 physicists
    for i in range(len(PR)):
        if titles[idx[-i-1]] in physicists:
            count+=1
            print('%d. %s = %f'%(count,titles[idx[-i-1]],PR[idx[-i-1]]))  
        if count ==20:
            break
#this physicist ranking is slow for some reason          
pagerank_wikipedia_demo()


