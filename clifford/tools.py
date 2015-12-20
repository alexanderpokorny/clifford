from warnings import warn
from . import Cl
def Mat2Frame(A, layout=None):
    '''
    Translates a [complex] matrix into a real frame
    
    The rows and columns are interpreted as follows
        * M,N = shape(A)
        * M = dimension of space
        * N = number of vectors
        
    If A is complex M and N are doubled.
    
    Parameters 
    ------------
    A : ndarray
        MxN matrix representing vectors 
    '''
    
    ## TODO: could simplify this by just implementing the real case 
    ## and then recursively calling this for A.real, and A.imag, then 
    ## combine results
    
    # M = dimension of space
    # N = number of vectors
    M,N = A.shape
    
    if A.dtype == 'complex':
        is_complex = True
        N = N*2
        M = M*2
        
    else:
        is_complex = False
    
    if layout is None:
        layout, blades = Cl(M,firstIdx=0)
        
    e_ = layout.basis_vectors()
    e_ = [e_['e%i'%k] for k in range(M)]
    
    a=[0^e_[0]]*N
    
    if not is_complex:
        for n in range(N):
            for m in range(M):
                a[n] = (a[n]) + ((A[m,n])^e_[m])
                
    else:
        for n in range(N/2):
            n_ = 2*n
            for m in range(M/2):
                m_ = 2*m
                
                a[n_] = (a[n_]) + ((A[m,n].real)^e_[m_]) \
                                + ((A[m,n].imag)^e_[m_+1])
                a[n_+1] = (a[n_+1]) + ((-A[m,n].imag)^e_[m_]) \
                                    + ((A[m,n].real)^e_[m_+1])
        
        
        
    return a, layout


def OrthoMat2Verser(A, eps= 1e-6,layout=None):
    '''
    Translates a [complex] orthogonal matrix to a Verser 
    '''
    B,layout = Mat2Frame(A,layout=layout)
    N = len(B)
    A,layout = Mat2Frame(eye(N),layout=layout)
    
    if (A.dot(A.conj().T) -eye(N)).max()>eps:
        warn('A doesnt appear to be a rotation. ')
    
    # store each reflector  in a list 
    rs = [1]*N
    
    for k in range(N):
        if abs((A[k]*B[k])-1) <eps:
            continue
        r = (A[k]-B[k])/abs(A[k]-B[k])
        for j  in range(k,N):
            A[j] = -r.inv()&A[j]&r

        rs[k] =r
    R = reduce(gp,rs )
    return R