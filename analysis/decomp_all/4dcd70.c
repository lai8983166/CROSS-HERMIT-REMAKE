
void FUN__text__004dcd70(undefined4 param_1,void *param_2)

{
  undefined4 uVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_50 [16];
  int local_10;
  undefined4 local_c;
  undefined *local_8;
  
  puVar3 = local_50;
  for (iVar2 = 0x13; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_8 = &DAT_006c4490;
  _memset(param_2,0,0x24);
  local_10 = (int)*(short *)(local_8 + 0x20);
  local_c = __ftol();
  uVar1 = FUN__text__004dbd70(local_c,0x7fffffff);
  *(undefined4 *)((int)param_2 + 0x20) = uVar1;
  local_8 = (undefined *)0x4dcdd8;
  FUN__text__0056ce80();
  return;
}

