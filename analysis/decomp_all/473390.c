
void FUN__text__00473390(short param_1,short param_2,undefined2 param_3,int param_4,uint param_5)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_48 [16];
  int local_8;
  
  puVar2 = local_48;
  for (iVar1 = 0x11; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  FUN__text__004077c0(DAT_007a49fc);
  *(char *)(local_8 + 0xde797) = (char)(param_5 >> 0x18);
  if (*(char *)(local_8 + 0xde797) == -1) {
    *(undefined4 *)(local_8 + 0xde78c) = 0;
  }
  else {
    *(undefined4 *)(local_8 + 0xde78c) = 1;
  }
  *(char *)(local_8 + 0xde796) = (char)((param_5 & 0xff0000) / 0x20000);
  *(char *)(local_8 + 0xde795) = (char)((param_5 & 0xff00) / 0x200);
  *(char *)(local_8 + 0xde794) = (char)((param_5 & 0xff) / 2);
  *(undefined2 *)(local_8 + 0xde7a6) = param_3;
  FUN__text__00407870(0x5a,0x14);
  *(ushort *)(local_8 + 0xde788) = *(ushort *)(local_8 + 0xde788) | 0x40;
  *(undefined2 *)(local_8 + 0xde768) = *(undefined2 *)(&DAT_00618958 + param_4 * 0xe0);
  *(undefined2 *)(local_8 + 0xde76a) = *(undefined2 *)(&DAT_0061895c + param_4 * 0xe0);
  *(undefined2 *)(local_8 + 0xde7a8) = *(undefined2 *)(&DAT_00618a00 + param_4 * 0xe0);
  *(undefined2 *)(local_8 + 0xde7aa) = *(undefined2 *)(&DAT_00618a04 + param_4 * 0xe0);
  *(short *)(local_8 + 0xde7ac) = *(short *)(local_8 + 0xde7a8) + *(short *)(local_8 + 0xde768);
  *(short *)(local_8 + 0xde7ae) = *(short *)(local_8 + 0xde7aa) + *(short *)(local_8 + 0xde76a);
  FUN__text__004079c0((int)param_1,(int)param_2);
  local_8 = 0x473564;
  FUN__text__0056ce80();
  return;
}

