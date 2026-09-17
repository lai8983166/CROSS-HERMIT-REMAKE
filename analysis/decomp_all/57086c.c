
void FUN_0057086c(void)

{
  code *pcVar1;
  int iVar2;
  int unaff_EBP;
  undefined4 *unaff_FS_OFFSET;
  
  iVar2 = FUN_00573780(0,0,0,0,&DAT_00592a18,"Object dump complete.\n");
  if (iVar2 != 1) {
    *unaff_FS_OFFSET = *(undefined4 *)(unaff_EBP + -0x10);
    return;
  }
  pcVar1 = (code *)swi(3);
  (*pcVar1)();
  return;
}

