USE [SchemaCheck]
GO

/****** Object:  Table [dbo].[SUBJECT_TABLE_STG_STUB]    Script Date: 11-01-2024 04:18:36 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[SUBJECT_TABLE_STG_STUB](
	[ID] [uniqueidentifier] NOT NULL,
	[STATUS] [char](10) NOT NULL,
	[STATUSTIMESTAMP] [timestamp] NOT NULL
) ON [PRIMARY]
GO

ALTER TABLE [dbo].[SUBJECT_TABLE_STG_STUB] ADD  DEFAULT ('LOADED') FOR [STATUS]
GO


