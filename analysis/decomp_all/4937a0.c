
void __fastcall FUN__text__004937a0(int param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_50 [16];
  undefined2 *local_10;
  int local_c;
  int local_8;
  
  puVar2 = local_50;
  for (iVar1 = 0x13; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_8 = param_1;
  for (local_c = 0; local_c != 5; local_c = local_c + 1) {
    _memset((void *)(local_8 + 0x116254 + local_c * 0x524),0,0x524);
    local_10 = (undefined2 *)(local_8 + 0x116258 + local_c * 0x524);
    *local_10 = 1;
    *(undefined4 *)(local_10 + 0x22) = *(undefined4 *)(local_8 + 0x2a6e8);
    FUN__text__00409ef0(local_10 + 0x24);
  }
  *(undefined4 *)(local_8 + 0x116250) = 0;
  local_8 = 0x493853;
  FUN__text__0056ce80();
  return;
}

