
void FUN__text__00483c00(int param_1,undefined4 param_2,int param_3)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_4c [16];
  char local_c;
  undefined4 local_8;
  
  puVar2 = local_4c;
  for (iVar1 = 0x12; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_c = *(char *)(param_3 + 7);
  if (local_c == '\0') {
    *(char *)(param_3 + 7) = *(char *)(param_3 + 7) + '\x01';
    *(char *)(param_3 + 8) =
         (char)((int)((*(int *)(param_1 + 0x2ec) >> 0x10) +
                     (*(int *)(param_1 + 0x2ec) >> 0x1f & 0x1fU)) >> 5);
    *(char *)(param_3 + 9) =
         (char)((int)((*(int *)(param_1 + 0x2f0) >> 0x10) +
                     (*(int *)(param_1 + 0x2f0) >> 0x1f & 0xfU)) >> 4);
    FUN__text__0046beb0(param_1,0xbbf,0,0,0,param_3);
  }
  local_8 = 0x483c9a;
  FUN__text__0056ce80();
  return;
}

