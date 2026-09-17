
void __fastcall FUN__text__0046b670(int param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_90 [32];
  int *local_10;
  int local_c;
  int local_8;
  
  puVar2 = local_90;
  for (iVar1 = 0x23; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_10 = (int *)(param_1 + 0xdc8ec);
  local_8 = param_1;
  for (local_c = 0; local_c != *local_10; local_c = local_c + 1) {
    FUN__text__0046cbd0(local_10[local_c + 1]);
  }
  FUN__text__0046da80();
  FUN__text__004952a0();
  FUN__text__00472a70(800);
  FUN__text__00491680(1);
  FUN__text__0049cce0();
  FUN__text__00482150();
  FUN__text__0049a600();
  FUN__text__00499b80();
  FUN__text__0049beb0();
  FUN__text__0049c850();
  FUN__text__00466910();
  FUN__text__00493b80();
  FUN__text__004936a0();
  local_8 = 0x46b74e;
  FUN__text__0056ce80();
  return;
}

