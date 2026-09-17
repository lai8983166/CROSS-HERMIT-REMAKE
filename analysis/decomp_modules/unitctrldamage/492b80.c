
void FUN__text__00492b80(undefined4 param_1,undefined4 param_2)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_a0 [16];
  undefined1 local_60 [44];
  undefined1 local_34 [44];
  undefined4 local_8;
  
  puVar2 = local_a0;
  for (iVar1 = 0x27; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  FUN__text__004deaa0(param_1,local_34);
  FUN__text__0046b3e0(param_1,local_34);
  FUN__text__004deaa0(param_2,local_60);
  FUN__text__0046b3e0(param_2,local_60);
  FUN__text__0048c0e0(0x3a,param_1,param_2,local_34,local_60);
  local_8 = 0x492c0d;
  FUN__text__0056ce80();
  return;
}

