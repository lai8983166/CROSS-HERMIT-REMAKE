
void __fastcall FUN__text__00426640(int param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_4c [16];
  int local_c;
  int local_8;
  
  puVar2 = local_4c;
  for (iVar1 = 0x12; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_8 = param_1;
  local_c = FUN__text__00426a80(param_1 + 0x63c);
  if (local_c != 0) {
    FUN__text__00426bc0(local_8 + 0x63c,0x3f,local_c + -1);
  }
  local_8 = 0x42669f;
  FUN__text__0056ce80();
  return;
}

