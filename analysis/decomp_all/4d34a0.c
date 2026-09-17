
void __fastcall FUN__text__004d34a0(undefined4 param_1)

{
  short sVar1;
  int iVar2;
  undefined2 extraout_var;
  undefined4 *puVar3;
  undefined4 local_4c [16];
  short local_c;
  undefined4 local_8;
  
  puVar3 = local_4c;
  for (iVar2 = 0x12; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_8 = param_1;
  for (local_c = 1; local_c < 0x2d; local_c = local_c + 1) {
    sVar1 = FUN__text__004d46e0(local_c);
    if (sVar1 != 0) {
      FUN__text__004d33a0(CONCAT22(extraout_var,local_c));
    }
  }
  local_8 = 0x4d350a;
  FUN__text__0056ce80();
  return;
}

