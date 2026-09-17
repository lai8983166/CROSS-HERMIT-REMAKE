
void Unwind_0058ed19(void)

{
  int unaff_EBP;
  
  if (*(int *)(unaff_EBP + -0x10) == 0) {
    *(undefined4 *)(unaff_EBP + -0x30) = 0;
  }
  else {
    *(int *)(unaff_EBP + -0x30) = *(int *)(unaff_EBP + -0x10) + 0x44;
  }
  FUN_004175a0();
  return;
}

