
void FUN__text__004e3070(undefined4 param_1)

{
  undefined4 uVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_14c [16];
  undefined4 local_10c;
  undefined1 local_108 [248];
  undefined4 uStack_10;
  
  puVar3 = local_14c;
  for (iVar2 = 0x52; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  uVar1 = FUN__text__004500b0("Option.bin");
  (*API_KERNEL32_DLL_lstrcpyA)(local_108,uVar1);
  FUN__text__0056ce80();
  local_10c = FUN__text__0042aec0(local_108,param_1,0x28);
  uStack_10 = 0x4e30e6;
  FUN__text__0056ce80();
  return;
}

