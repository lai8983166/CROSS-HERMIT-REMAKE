
void FUN__text__004e2f50(void)

{
  undefined4 uVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_154 [16];
  int local_114;
  int local_110;
  int local_10c;
  undefined1 local_108 [248];
  undefined4 uStack_10;
  
  puVar3 = local_154;
  for (iVar2 = 0x54; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_10c = 0;
  uVar1 = FUN__text__004500b0("Option.bin");
  (*API_KERNEL32_DLL_lstrcpyA)(local_108,uVar1);
  FUN__text__0056ce80();
  iVar2 = FUN__text__0042a8e0(local_108);
  if ((((((iVar2 == 0) || (local_10c = FUN__text__0042ae70(local_108,&local_110), local_110 != 0x28)
         ) || (*(int *)(local_10c + 0x1c) < 0)) ||
       ((9 < *(int *)(local_10c + 0x1c) || (*(int *)(local_10c + 0x20) < 0)))) ||
      ((9 < *(int *)(local_10c + 0x20) ||
       ((*(int *)(local_10c + 0x24) < 0 || (9 < *(int *)(local_10c + 0x24))))))) && (local_10c == 0)
     ) {
    local_114 = local_10c;
    FUN__text__00428ad0(0);
  }
  uStack_10 = 0x4e306b;
  FUN__text__0056ce80();
  return;
}

