
void __fastcall FUN__text1__008202b3(undefined4 param_1,undefined2 param_2)

{
  undefined4 uVar1;
  int unaff_EBP;
  
  in(param_2);
  uVar1 = (*(code *)PTR_DAT_00872c8c)(*(undefined4 *)(unaff_EBP + 8));
  *(undefined4 *)(unaff_EBP + -4) = uVar1;
  *(uint *)(unaff_EBP + -0xc) = (uint)((*(uint *)(unaff_EBP + -4) & 0x40) == 0);
  *(uint *)(unaff_EBP + -8) = (DAT_0086e3bc ^ DAT_0086e3c0) << 1;
  if (*(int *)(unaff_EBP + -0xc) != 0) {
    *(uint *)(unaff_EBP + -8) = *(uint *)(unaff_EBP + -8) | 1;
  }
  (*(code *)PTR_DAT_00872c3c)(*(undefined4 *)(unaff_EBP + -8));
  return;
}

