
void __fastcall FUN__text__004260b0(int param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_50 [16];
  undefined1 local_10 [8];
  int local_8;
  
  puVar2 = local_50;
  for (iVar1 = 0x13; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  if (*(int *)(param_1 + 8) != 0) {
    local_8 = param_1;
    FUN__text__0056cd62(*(undefined4 *)(param_1 + 8),0x20,local_10,8);
  }
  local_8 = 0x426106;
  FUN__text__0056ce80();
  return;
}

