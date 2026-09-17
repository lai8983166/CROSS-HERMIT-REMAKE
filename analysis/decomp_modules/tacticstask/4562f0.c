
void __fastcall FUN__text__004562f0(int param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_4c [16];
  void *local_c;
  int local_8;
  
  puVar2 = local_4c;
  for (iVar1 = 0x12; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_c = (void *)(*(int *)(param_1 + 0x60) + 0x2434);
  local_8 = param_1;
  _memset(local_c,0,0x1c);
  local_8 = 0x456339;
  FUN__text__0056ce80();
  return;
}

