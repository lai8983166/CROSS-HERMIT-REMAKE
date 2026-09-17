
void __fastcall FUN__text__00496490(int param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_4c [16];
  char local_c;
  int local_8;
  
  puVar2 = local_4c;
  for (iVar1 = 0x12; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_c = *(char *)(param_1 + 0x117c3c);
  local_8 = param_1;
  if (local_c == '\x01') {
    FUN__text__004964f0();
  }
  else if (local_c == '\x02') {
    FUN__text__004968b0();
  }
  local_8 = 0x4964e8;
  FUN__text__0056ce80();
  return;
}

