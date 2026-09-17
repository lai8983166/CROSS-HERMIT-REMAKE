
void FUN__text__00574e5d(void)

{
  int iVar1;
  int unaff_EBP;
  
  *(undefined4 *)(*(int *)(unaff_EBP + 0xc) + -4) = *(undefined4 *)(unaff_EBP + -0x28);
  iVar1 = FUN__text__005753b0();
  *(undefined4 *)(iVar1 + 0x6c) = *(undefined4 *)(unaff_EBP + -0x1c);
  iVar1 = FUN__text__005753b0();
  *(undefined4 *)(iVar1 + 0x70) = *(undefined4 *)(unaff_EBP + -0x20);
  if ((((**(int **)(unaff_EBP + 8) == -0x1f928c9d) &&
       (*(int *)(*(int *)(unaff_EBP + 8) + 0x10) == 3)) &&
      (*(int *)(*(int *)(unaff_EBP + 8) + 0x14) == 0x19930520)) &&
     ((*(int *)(unaff_EBP + -0x24) == 0 && (*(int *)(unaff_EBP + -0x2c) != 0)))) {
    iVar1 = __abnormal_termination();
    ___DestructExceptionObject(*(undefined4 *)(unaff_EBP + 8),iVar1);
  }
  return;
}

