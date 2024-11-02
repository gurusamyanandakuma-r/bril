#include "llvm/Pass.h"
#include "llvm/IR/Function.h"
#include "llvm/Support/raw_ostream.h"
#include "llvm/IR/LegacyPassManager.h"
#include "llvm/Transforms/IPO/PassManagerBuilder.h"
#include "llvm/IR/Instructions.h"

using namespace llvm;

namespace {
struct DivCheckPass : public FunctionPass {
    static char ID;
    DivCheckPass() : FunctionPass(ID) {}

    bool runOnFunction(Function &F) override {
        errs() << "Analyzing Function: " << F.getName() << "\n";
        
        for (auto &BB : F) {
            errs() << "  Basic Block: ";
            BB.printAsOperand(errs(), false);
            errs() << "\n";
            
            for (auto &I : BB) {
                if (auto *BO = dyn_cast<BinaryOperator>(&I)) {
                    if (BO->getOpcode() == Instruction::SDiv ||
                        BO->getOpcode() == Instruction::UDiv) {
                        errs() << "    Found division instruction: ";
                        I.print(errs());
                        errs() << "\n";
                    }
                }
            }
        }
        
        return false;
    }
};
}

char DivCheckPass::ID = 0;

// Register the pass
static RegisterPass<DivCheckPass> 
X("divcheck", "Division Check Pass",
  false /* Only looks at CFG */,
  false /* Analysis Pass */);

static RegisterStandardPasses Y(
    PassManagerBuilder::EP_EarlyAsPossible,
    [](const PassManagerBuilder &Builder,
       legacy::PassManagerBase &PM) { PM.add(new DivCheckPass()); });