from algorithm import vectorize, parallelize
from sys.info import simdwidthof
import time

alias type = DType.float32
alias width = simdwidthof[type]()

# A reference high-performance MatMul kernel for Mojo
# Demonstrates 1D vectorization + Tiling approach
fn matmul_simd(
    C: DTypePointer[type], 
    A: DTypePointer[type], 
    B: DTypePointer[type], 
    M: Int, N: Int, K: Int
):
    @parameter
    fn calc_row(m: Int):
        for k in range(K):
            @parameter
            fn dot[simd_width: Int](n: Int):
                # Load a vector of B's row and multiply by A's scalar value
                let a_val = A.load(m * K + k)
                let b_vec = B.load[simd_width](k * N + n)
                let c_vec = C.load[simd_width](m * N + n)
                C.store[simd_width](m * N + n, c_vec + a_val * b_vec)
            
            vectorize[width, dot](N)

    parallelize[calc_row](M)

fn main():
    print("--- Mojo SIMD MatMul Benchmark ---")
    let M = 1024
    let N = 1024
    let K = 1024
    
    let A = DTypePointer[type].alloc(M * K)
    let B = DTypePointer[type].alloc(K * N)
    let C = DTypePointer[type].alloc(M * N)
    
    # Initialize (omitted for brevity)
    
    let start = time.now()
    matmul_simd(C, A, B, M, N, K)
    let end = time.now()
    
    let duration = (end - start) / 1e9
    let gflops = (2.0 * M * N * K) / duration / 1e9
    print("Mojo SIMD GFLOPS:", gflops)
