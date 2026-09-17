
void FUN__text__004e2da0(undefined4 param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_48 [16];
  undefined4 local_8;
  
  puVar2 = local_48;
  for (iVar1 = 0x11; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  if (DAT_007a49fc != 0) {
    local_8 = FUN__text__004e2ec0(param_1);
    FUN__text__0041da10(local_8);
  }
  local_8 = 0x4e2df2;
  FUN__text__0056ce80();
  return;
}

