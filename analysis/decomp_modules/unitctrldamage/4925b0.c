
void FUN__text__004925b0(undefined4 param_1,undefined4 param_2,int param_3)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_a4 [16];
  byte local_64;
  undefined1 local_60 [44];
  undefined1 local_34 [44];
  undefined4 local_8;
  
  puVar2 = local_a4;
  for (iVar1 = 0x28; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  if (*(char *)(param_3 + 6) != '\x04') {
    FUN__text__00493090(param_2,*(undefined2 *)(param_3 + 10),0);
  }
  local_64 = *(byte *)(param_3 + 6);
  if ((local_64 != 0) && (local_64 < 4)) {
    FUN__text__004deaa0(param_1,local_34);
    FUN__text__0046b3e0(param_1,local_34);
    FUN__text__004deaa0(param_2,local_60);
    FUN__text__0046b3e0(param_2,local_60);
    FUN__text__0048b900(0x14,param_1,param_2,local_34,local_60);
  }
  local_8 = 0x492677;
  FUN__text__0056ce80();
  return;
}

