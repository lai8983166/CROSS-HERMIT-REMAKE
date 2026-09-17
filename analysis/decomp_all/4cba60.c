
void __fastcall FUN__text__004cba60(char *param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_4c [16];
  int local_c;
  char *local_8;
  
  puVar2 = local_4c;
  for (iVar1 = 0x12; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  if (*param_1 == '\x01') {
    local_c = (byte)param_1[1] - 1;
    local_8 = param_1;
    switch(local_c) {
    case 0:
      FUN__text__004d2ba0(0x15,*(undefined2 *)(param_1 + 4),*(undefined2 *)(param_1 + 2),
                          (int)*(short *)(param_1 + 6),(int)*(short *)(param_1 + 8));
      break;
    case 1:
      FUN__text__004d2ca0(0x15,*(undefined2 *)(param_1 + 4),*(undefined2 *)(param_1 + 2),
                          (int)*(short *)(param_1 + 6),(int)*(short *)(param_1 + 8),
                          (int)*(short *)(param_1 + 0xe),(int)*(short *)(param_1 + 0x10),
                          (int)*(short *)(param_1 + 0x12),(int)*(short *)(param_1 + 0x14));
      break;
    case 2:
      FUN__text__004d2dd0(0x15,*(undefined2 *)(param_1 + 4),*(undefined2 *)(param_1 + 2),
                          (int)*(short *)(param_1 + 6),(int)*(short *)(param_1 + 8),
                          (int)*(short *)(param_1 + 0xe),(int)*(short *)(param_1 + 0x10),
                          (int)*(short *)(param_1 + 0x12),(int)*(short *)(param_1 + 0x14),
                          (int)*(short *)(param_1 + 0x16),(int)*(short *)(param_1 + 0x18));
      break;
    case 3:
      FUN__text__004d3050(0x15,*(undefined2 *)(param_1 + 4),*(undefined2 *)(param_1 + 2),
                          (int)*(short *)(param_1 + 6),(int)*(short *)(param_1 + 8),
                          (int)*(short *)(param_1 + 0xe),(int)*(short *)(param_1 + 0x10),
                          (int)*(short *)(param_1 + 0x12),(int)*(short *)(param_1 + 0x14),
                          param_1[0xd],param_1[10],param_1[0xb],param_1[0xc]);
      break;
    case 4:
      FUN__text__004d30c0(0x15,*(undefined2 *)(param_1 + 4),*(undefined2 *)(param_1 + 2),
                          (int)*(short *)(param_1 + 6),(int)*(short *)(param_1 + 8),param_1[0xd],
                          param_1[10],param_1[0xb],param_1[0xc]);
    }
  }
  local_8 = (char *)0x4cbc86;
  FUN__text__0056ce80();
  return;
}

