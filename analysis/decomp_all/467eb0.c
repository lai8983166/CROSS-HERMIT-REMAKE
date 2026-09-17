
void __fastcall FUN__text__00467eb0(int param_1)

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
  _memset((void *)(param_1 + 0x2a6e8),0,8);
  _memset((void *)(local_8 + 0x2a6f0),0,0x1000);
  _memset((void *)(local_8 + 0x80aec),0,0x50140);
  _memset((void *)(local_8 + 0xd0c2c),0,44000);
  _memset((void *)(local_8 + 0xdb86c),0,0xaa0);
  _memset((void *)(local_8 + 0x115cba),0,0x5a);
  FUN__text__00492e90();
  FUN__text__00494d20();
  *(undefined4 *)(local_8 + 0x108f74) = 0;
  *(undefined2 *)(local_8 + 0x108b32) = 0;
  *(undefined2 *)(local_8 + 0x10f9c2) = 0xffff;
  *(undefined2 *)(local_8 + 0x10f9c0) = 0xffff;
  *(undefined1 *)(local_8 + 0x10f9c4) = 0;
  *(undefined4 *)(local_8 + 0xdb868) = 0;
  for (local_c = 0; local_c != 0x10; local_c = local_c + 1) {
    *(undefined2 *)(local_8 + 0x2ef14 + local_c * 2) = 0;
  }
  for (local_c = 0; local_c != 0x10; local_c = local_c + 1) {
    *(undefined1 *)(local_8 + local_c + 0x2ef34) = 0;
  }
  _memset((void *)(local_8 + 0x2e714),0,0x800);
  FUN__text__00468bc0();
  iVar1 = FUN__text__00456b20();
  if (iVar1 != 0) {
    FUN__text__00468c00();
  }
  FUN__text__004671f0();
  FUN__text__00467380();
  FUN__text__00467520();
  FUN__text__004676c0();
  FUN__text__004077c0(DAT_007a49fc);
  FUN__text__0042b2d0("UNIT_DATA : SIZE = %d\n",0xb0);
  FUN__text__0042b2d0("UNIT_WORK : SIZE = %d\n",0x520);
  local_8 = 0x4680a7;
  FUN__text__0056ce80();
  return;
}

